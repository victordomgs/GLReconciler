import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

def generar_datos_demo(n_transacciones=80, seed=42):
    random.seed(seed); np.random.seed(seed)
    
    fechas = [date(2024, 3, 1) + timedelta(days=i % 31) for i in range(n_transacciones)]
    importes = np.round(np.random.uniform(500, 50000, n_transacciones), 2)
    refs = [f"TXN-{1000+i}" for i in range(n_transacciones)]
    conceptos = random.choices(["Proveedor A", "Nómina", "Alquiler", "Servicios IT", "Seguros"], k=n_transacciones)

    banco = pd.DataFrame({"fecha": fechas, "referencia": refs, "concepto": conceptos, "importe": importes})

    # GL: introduce 4 tipos de breaks deliberados
    gl_importes = importes.copy()
    gl_refs = refs.copy()
    gl_fechas = list(fechas)

    # Break tipo 1: diferencia de importe (error tipográfico)
    for i in [5, 23, 47]:
        gl_importes[i] = round(importes[i] + random.choice([-0.01, 0.01, 100, -100]), 2)

    # Break tipo 2: referencia duplicada
    gl_refs[12] = refs[11]

    # Break tipo 3: transacción en GL pero no en banco (asiento anticipado)
    extra = pd.DataFrame({"fecha": [date(2024, 3, 15)], "referencia": ["TXN-9999"],
                          "concepto": ["Ajuste manual"], "importe": [1250.00]})

    # Break tipo 4: fecha desplazada (timing difference)
    gl_fechas[31] = fechas[31] + timedelta(days=1)

    gl = pd.DataFrame({"fecha": gl_fechas, "referencia": gl_refs, "concepto": conceptos, "importe": gl_importes})
    gl = pd.concat([gl, extra], ignore_index=True)

    banco.to_csv("data/banco_marzo.csv", index=False)
    gl.to_csv("data/libro_mayor_marzo.csv", index=False)
    print(f"Generados: {len(banco)} registros banco, {len(gl)} registros GL")
    print("Breaks plantados: 3 diferencias de importe, 1 duplicado de ref, 1 asiento extra, 1 timing difference")

generar_datos_demo()