# GL Reconciler — Agente de Conciliación Contable

Demo de agente de IA para la detección y análisis automático de breaks en procesos de conciliación entre extractos bancarios y libros mayores (GL). Construido con Claude (Anthropic) y Streamlit.

---

## ¿Qué hace?

Este agente automatiza el proceso de conciliación contable en tres pasos:

1. **Ingesta y cruce** — carga el extracto bancario y el libro mayor en formato CSV, los normaliza y los cruza por referencia de transacción.
2. **Detección de breaks** — identifica discrepancias de cuatro tipos: diferencias de importe, asientos huérfanos, transacciones faltantes en GL y duplicados de referencia.
3. **Análisis con IA** — Claude clasifica la causa raíz de cada break, asigna urgencia (alta/media/baja) y sugiere la acción correctora. Genera un resumen ejecutivo para el director financiero.
4. **Human-in-the-loop** — el usuario puede aprobar la conciliación o escalarla al responsable financiero.

---

## Tecnologías

- [Claude API](https://console.anthropic.com) (Anthropic) — análisis y clasificación de breaks
- [Streamlit](https://streamlit.io) — interfaz web interactiva
- [Pandas](https://pandas.pydata.org) — procesamiento y cruce de datos
- Python 3.12+

---

## Estructura del proyecto

```
gl-reconciler/
├── src/
│   ├── generate_data.py   # Generador de datos sintéticos para demo
│   ├── agent.py           # Lógica del agente: detección y análisis con Claude
│   └── app.py             # Interfaz Streamlit
├── data/                  # CSVs generados (no incluidos en el repo)
├── .env                   # API key (no incluido en el repo)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/victordomgs/GLReconciler.git
cd GLReconciler
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Configura tu API key

Crea un archivo `.env` en la raíz del proyecto:

```
ANTHROPIC_API_KEY=sk-ant-tu-api-key-aqui
```

Puedes obtener tu API key en [console.anthropic.com](https://console.anthropic.com).

### 4. Genera los datos sintéticos de demo

```bash
python src/generate_data.py
```

Esto creará `banco_marzo.csv` y `libro_mayor_marzo.csv` en la carpeta `data/` con breaks intencionados para demostrar el agente.

---

## Uso

Lanza la aplicación:

```bash
python -m streamlit run src/app.py
```

Abre el navegador en `http://localhost:8501` y sube los dos CSVs para comenzar.

---

## Tipos de breaks detectados

| Tipo | Descripción |
|------|-------------|
| `diferencia_importe` | El importe no coincide entre banco y GL |
| `asiento_huerfano` | Asiento en GL sin movimiento bancario correspondiente |
| `falta_en_gl` | Transacción bancaria sin asiento en GL |
| `duplicado_referencia` | Referencia duplicada en GL |

---

## Licencia

MIT License — puedes usar, modificar y distribuir este proyecto libremente.

---

*Desarrollado como demo de agente de IA aplicado al sector financiero.*
