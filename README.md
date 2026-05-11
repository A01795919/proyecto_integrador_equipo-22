# Proyecto Integrador — Equipo 22

## Identificación de biomarcadores lipidómicos y metabolómicos para la detección temprana de cáncer colorrectal mediante modelos predictivos de inteligencia artificial

> **Avance 1 — Análisis Exploratorio de Datos (EDA)**
> Proyecto Integrador · Maestría en Ciencia de Datos · Tecnológico de Monterrey

---

## Equipo

| Nombre | Matrícula |
|---|---|
| María Virginia Mendizábal Miranda | A01796588 |
| Gianmel Joannelly Hernandez Tosta | A01795919 |
| Sofía Ordaz López | A01173717 |

---

## Resumen del proyecto

El cáncer colorrectal (CRC) constituye la tercera causa de cáncer a nivel mundial y la segunda causa de muerte por cáncer. La detección temprana — particularmente en la etapa de adenoma avanzado (AA), precursora del adenocarcinoma — es determinante para reducir la mortalidad y mejorar los desenlaces clínicos. El presente proyecto explora si los perfiles lipidómicos y metabolómicos extraídos de muestras fecales mediante UHPLC-MS contienen señal discriminante suficiente para construir un clasificador supervisado de tres clases (Control sano / Adenoma avanzado / Cáncer colorrectal).

El conjunto de datos (211 observaciones × 127 lípidos cuantificados, más variables clínicas) corresponde a la cohorte del Hospital Universitario de Ourense (Galicia, España) reportada en Albóniga et al. (2025), *Cancers*, 17, 2339. La presente entrega documenta el **Análisis Exploratorio de Datos** completo, fase preparatoria a la construcción del modelo predictivo.

---

## Estructura del repositorio

```
proyecto_integrador_equipo-22/
│
├── README.md                                # Este documento
├── requirements.txt                          # Dependencias de Python
├── .gitignore                                # Archivos excluidos del control de versiones
│
├── notebooks/
│   └── eda_crc.ipynb                         # Análisis Exploratorio de Datos completo
│
├── data/
│   └── BASE DE DATOS CRC PROYECT LABELED(Data Mat).csv   # Conjunto de datos (CC BY 4.0)
│
├── docs/
│   ├── memorando_hallazgos_lipidomicos.md    # Memorando para el equipo biomédico (fuente)
│   └── memorando_hallazgos_lipidomicos.pdf   # Memorando para el equipo biomédico (PDF)
│
└── references/
    └── Alboniga_etal_2025_Cancers_17_2339.pdf   # Artículo de procedencia del dataset
```

---

## Reproducibilidad

### Requisitos previos

- Python 3.10 o superior
- Git

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/A01795919/proyecto_integrador_equipo-22.git
cd proyecto_integrador_equipo-22

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate         # macOS / Linux
# .venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Registrar el kernel de Jupyter (opcional)
python -m ipykernel install --user --name=proyecto-integrador-crc --display-name="Python (Proyecto CRC)"
```

### Ejecución de la libreta

```bash
# Opción 1: Abrir Jupyter Notebook
jupyter notebook notebooks/eda_crc.ipynb

# Opción 2: Abrir directamente en VS Code
code notebooks/eda_crc.ipynb
```

La libreta detecta automáticamente la ubicación del conjunto de datos y se ejecuta de inicio a fin sin necesidad de modificaciones manuales. Tiempo aproximado de ejecución completa: 2–3 minutos.

> **Importante:** la libreta está diseñada para ejecutarse **secuencialmente** (de inicio a fin) según los lineamientos de entrega.

---

## Mapeo de la libreta a los criterios de evaluación

La libreta `notebooks/eda_crc.ipynb` está organizada para abordar de forma explícita los cinco criterios de la rúbrica del Avance 1:

| Criterio (20 pts c/u) | Secciones de la libreta | Contenido |
|---|---|---|
| **1. Estructura de los datos** | Paso 1 (1.1–4) · Paso 2.4 | Forma del conjunto, tipos de datos, reconstrucción de encabezados anidados, distribución de la variable objetivo, cardinalidad de variables categóricas |
| **2. Análisis univariante** | Paso 2.1 · Paso 3.1 · Paso 3.2 | Histogramas y diagramas de caja para variables clínicas, análisis de asimetría sobre los 127 lípidos, diagramas Q-Q comparativos |
| **3. Análisis bi/multivariante** | Paso 4.3–4.6 · Paso 5.1–5.4 | Análisis pareado (Wilcoxon-Mann-Whitney) con tres comparaciones binarias, mapa de calor de correlación agrupado por familia, PCA con elipses de confianza, PLS-DA con cálculo de VIP scores, atributos estructurales derivados |
| **4. Preprocesamiento** | Paso 2.1.4 · Paso 3.3 · Paso 3.4 · Paso 3.5 | Imputación por mediana de grupo (justificada por test χ²), evaluación comparativa de cuatro transformaciones (raw, log1p, Yeo-Johnson, Box-Cox), detección de valores atípicos mediante MAD post-transformación |
| **5. Conclusiones** | Conclusiones del análisis exploratorio · `docs/memorando_hallazgos_lipidomicos.pdf` | Síntesis narrativa de los hallazgos, replicación íntegra de biomarcadores reportados por Albóniga et al. (2025), implicaciones para la fase de modelado, memorando complementario para discusión con el equipo biomédico |

---

## Hallazgos principales del EDA

### Calidad del conjunto de datos

- **211 observaciones × 127 lípidos** con distribución por grupo: CTRL 78, AA 58, CRC 75 (desbalance leve, ratio 1.34).
- Se identificó un patrón de valores faltantes **dependiente del grupo** (test χ², 13/56 lípidos con p < 0.05). La ausencia es consistente con concentraciones por debajo del límite de detección del instrumento UHPLC-MS, fenómeno biológicamente informativo. La estrategia de imputación adoptada (mediana por grupo) preserva esta señal.

### Transformación de datos

- Las 127 variables lipídicas presentan asimetría muy fuerte en datos crudos (mediana de skewness = 5.47).
- Se evaluaron formalmente cuatro transformaciones: raw, log1p, Yeo-Johnson y Box-Cox. La transformación **Box-Cox** demostró superioridad cuantitativa al normalizar el 81.1% de las variables (test Shapiro-Wilk, p > 0.05), frente al 5.5% con Yeo-Johnson y al 0.8% con log1p.

### Biomarcadores identificados

- **42 lípidos** estadísticamente significativos en el análisis multigrupo (Kruskal-Wallis, q < 0.05).
- **Replicación íntegra del 100%** de los biomarcadores reportados por Albóniga et al. (2025): 7/7 en CRC vs CTRL (Tabla 3) y 5/5 en CRC vs AA (Tabla 4).
- **`CE(20:4)`** se confirma como el biomarcador con mayor poder discriminativo (log₂ fold-change = +2.56, q = 7.4 × 10⁻¹⁰).

### Caracterización de la dificultad del problema

- La discriminación es asimétrica entre las tres clases: 38 biomarcadores significativos en CRC vs CTRL, 30 en CRC vs AA, pero únicamente **6 en AA vs CTRL**.
- El adenoma avanzado (AA) resulta lipidómicamente cercano al control sano, lo cual cuantifica la dificultad clínica de la detección temprana.

### Aporte diferencial al estudio original

- **`plasmalogen_frac`** — atributo derivado que agrega la fracción de plasmalógenos por observación — emerge como el **único feature** donde CRC se separa estadísticamente de **ambos** CTRL y AA, mientras AA y CTRL permanecen indistinguibles (p = 0.96). Sugiere un marcador específico del momento de transición carcinogénica.
- Validación independiente del procedimiento de detección de valores atípicos: **6 de las 12 muestras anómalas** identificadas en la Figura S2 del estudio original son detectadas por nuestra metodología (z robusto MAD post-Box-Cox), pese a emplear un método distinto al del estudio.

---

## Próximos pasos

El presente entregable corresponde al Avance 1 (Análisis Exploratorio de Datos). Los avances subsecuentes contemplarán:

1. **Construcción del modelo predictivo supervisado** para el problema multiclase CTRL/AA/CRC, evaluando Logistic Regression, Random Forest, SVM RBF y PLS-DA.
2. **Comparación de pipelines con y sin variables clínicas** (FIT, FOB), para cuantificar el aporte real de la lipidómica más allá del estándar clínico.
3. **Validación cruzada estratificada** con reporte de F1-macro, AUC One-vs-Rest y matrices de confusión completas.
4. **Integración del feedback biomédico** del equipo interdisciplinario sobre los hallazgos contenidos en [`docs/memorando_hallazgos_lipidomicos.pdf`](docs/memorando_hallazgos_lipidomicos.pdf).

---

## Procedencia del conjunto de datos

El conjunto `BASE DE DATOS CRC PROYECT LABELED(Data Mat).csv` se obtuvo del Supplementary File S1 (`MX_SuppTable.xlsx`, hoja `DataMat`) del artículo:

> Albóniga, O. E., Cubiella, J., Bujanda, L., Aspichueta, P., Blanco, M. E., Lanza, B., Alonso, C., & Falcón-Pérez, J. M. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, *17*(14), 2339. https://doi.org/10.3390/cancers17142339

El artículo y los materiales suplementarios se distribuyen bajo licencia **Creative Commons Attribution 4.0 (CC BY 4.0)**, lo que permite su redistribución con atribución apropiada.

---

## Referencias metodológicas

- Albóniga, O. E. et al. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, *17*(14), 2339.
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B*, *57*(1), 289–300.
- Box, G. E. P., & Cox, D. R. (1964). An analysis of transformations. *Journal of the Royal Statistical Society: Series B*, *26*(2), 211–252.
- Brownlee, J. (2020). *How to choose a feature selection method for machine learning*. Machine Learning Mastery.
- Costa, R. (2022). *The CRISP-ML methodology: A step-by-step approach to real-world machine learning projects*.
- Galli, S. (2022). *Python feature engineering cookbook* (2.ª ed.). Packt Publishing.
- Huang, C. Y., & Dai, H. L. (2021). Learning from class-imbalanced data: Review of data driven methods and algorithm driven methods. *Data Science in Finance and Economics*, *1*(1), 26–36.
- Wold, S., Sjöström, M., & Eriksson, L. (2001). PLS-regression: A basic tool of chemometrics. *Chemometrics and Intelligent Laboratory Systems*, *58*(2), 109–130.

---

## Licencia y uso

Este repositorio constituye trabajo académico desarrollado en el marco del Proyecto Integrador de la Maestría en Ciencia de Datos del Tecnológico de Monterrey. El conjunto de datos y el artículo de referencia se redistribuyen bajo Creative Commons Attribution 4.0. El código y la documentación propia de este repositorio quedan sujetos a uso académico.

---

**Última actualización:** mayo de 2026
