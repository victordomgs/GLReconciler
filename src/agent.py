# -*- coding: utf-8 -*-
import anthropic
import pandas as pd
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def detectar_breaks(banco_path, gl_path):
    banco = pd.read_csv(banco_path)
    gl = pd.read_csv(gl_path)
    merged = banco.merge(gl, on="referencia", how="outer", suffixes=("_banco", "_gl"), indicator=True)
    breaks = []
    for _, r in merged[merged["_merge"] == "left_only"].iterrows():
        breaks.append({"ref": r["referencia"], "tipo": "falta_en_gl",
                       "importe_banco": r["importe_banco"], "importe_gl": None,
                       "detalle": "Falta en GL"})
    for _, r in merged[merged["_merge"] == "right_only"].iterrows():
        breaks.append({"ref": r["referencia"], "tipo": "asiento_huerfano",
                       "importe_banco": None, "importe_gl": r["importe_gl"],
                       "detalle": "Asiento huerfano"})
    ambos = merged[merged["_merge"] == "both"].copy()
    ambos["diferencia"] = (ambos["importe_banco"] - ambos["importe_gl"]).round(2)
    for _, r in ambos[ambos["diferencia"] != 0].iterrows():
        breaks.append({"ref": r["referencia"], "tipo": "diferencia_importe",
                       "importe_banco": r["importe_banco"], "importe_gl": r["importe_gl"],
                       "diferencia": r["diferencia"],
                       "detalle": "Diferencia de importe"})
    return {"total_banco": len(banco), "total_gl": len(gl),
            "breaks": breaks, "n_breaks": len(breaks)}

def analizar_con_claude(resultado):
    prompt = (
        "Eres un agente de conciliacion contable. "
        f"Breaks detectados: {resultado['n_breaks']}. "
        f"Detalle: {json.dumps(resultado['breaks'])}. "
        "Para cada break indica: 1) causa raiz probable "
        "2) urgencia alta/media/baja 3) accion correctora. "
        "Finaliza con resumen ejecutivo de 3 lineas."
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text