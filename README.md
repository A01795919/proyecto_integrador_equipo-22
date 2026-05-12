# Proyecto Integrador — Equipo 22

## Identificación de biomarcadores lipidómicos y metabolómicos para la detección temprana de cáncer colorrectal mediante modelos predictivos de inteligencia artificial

> **Avance 1 — Análisis Exploratorio de Datos (EDA)**
> Proyecto Integrador · Maestría en Inteligencia Artificial Aplicada · Tecnológico de Monterrey

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
├── requirements.txt                         # Dependencias de Python
├── .gitignore                               # Archivos excluidos del control de versiones
│
├── notebooks/
│   └── Avance1_Equipo22.ipynb               # Análisis Exploratorio de Datos completo
│
├── data/
│   └── BASE DE DATOS CRC PROYECT LABELED(Data Mat).csv   # Conjunto de datos (CC BY 4.0)
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
jupyter notebook notebooks/Avance1_Equipo22.ipynb

# Opción 2: Abrir directamente en VS Code
code notebooks/Avance1_Equipo22.ipynb
```

La libreta detecta automáticamente la ubicación del conjunto de datos y se ejecuta de inicio a fin sin necesidad de modificaciones manuales. Tiempo aproximado de ejecución completa: 2–3 minutos.

> **Importante:** la libreta está diseñada para ejecutarse **secuencialmente** (de inicio a fin) según los lineamientos de entrega.

---

## Mapeo de la libreta a los criterios de evaluación

La libreta `notebooks/Avance1_Equipo22.ipynb` está organizada para abordar de forma explícita los cinco criterios de la rúbrica del Avance 1:

| Criterio (20 pts c/u) | Secciones de la libreta | Contenido |
|---|---|---|
| **1. Estructura de los datos** | Paso 1 · Paso 2.3 | Forma del conjunto, tipos de datos, reconstrucción de encabezados anidados, diccionario de variables por familia, distribución de la variable objetivo, cardinalidad de variables categóricas |
| **2. Análisis univariante** | Paso 2.1 · Paso 3.1 · Paso 3.2 | Histogramas y diagramas de caja para variables clínicas, análisis de asimetría sobre los 127 lípidos, diagramas Q-Q comparativos por transformación |
| **3. Análisis bi/multivariante** | Paso 4 · Paso 5 | Selección supervisada de variables con `SelectKBest` (χ² sobre categóricas one-hot e información mutua sobre numéricas), mapa de calor de correlación agrupado por familia, PCA con elipses de confianza al 95%, atributos estructurales derivados evaluados con información mutua |
| **4. Preprocesamiento** | Paso 2.1.4 · Paso 3.3 · Paso 3.4 · Paso 3.5 | Imputación por mediana de grupo (justificada por test χ² y validada por matrices de correlación pre/post), evaluación comparativa de cuatro transformaciones (raw, log1p, Yeo-Johnson, Box-Cox), detección de valores atípicos mediante regla IQR sobre datos transformados |
| **5. Conclusiones** | Conclusiones del análisis exploratorio · Pipeline propuesto para Avance 2 | Síntesis narrativa por paso, ranking de variables candidatas al modelado, caracterización de la dificultad del problema multiclase a partir de PCA e información mutua, pipeline propuesto para la fase de modelado supervisado |

---

## Hallazgos principales del EDA

### Calidad del conjunto de datos

- **211 observaciones × 127 lípidos** con distribución por grupo: CTRL 78, AA 58, CRC 75 (desbalance leve, ratio 1.34).
- Se identificó un patrón de valores faltantes **dependiente del grupo** (test χ², 13 de 56 lípidos con p < 0.05). La ausencia es consistente con concentraciones por debajo del límite de detección del instrumento UHPLC-MS, fenómeno biológicamente informativo. La estrategia de imputación adoptada (mediana por grupo) preserva esta señal y se validó cuantitativamente mediante comparación de matrices de correlación pre y post-imputación.

### Transformación de datos

- Las 127 variables lipídicas presentan asimetría muy fuerte en datos crudos (mediana de skewness ≈ 5.5).
- Se evaluaron formalmente cuatro transformaciones: raw, log1p, Yeo-Johnson y Box-Cox. La transformación **Box-Cox** demostró superioridad cuantitativa al aproximar el 81.1% de las variables a la normalidad (test Shapiro-Wilk, p > 0.05), frente al 5.5% con Yeo-Johnson y al 0.8% con log1p.
- Sobre los datos transformados, la regla IQR de Tukey identifica 769 outliers sobre 25 742 celdas (≈ 3%), tasa coherente con una cohorte depurada.

### Selección supervisada de variables (Paso 4)

- **Categóricas (χ² sobre one-hot encoding):** `fob_YES` emerge como dominante (χ² = 23.9, p = 6.5 × 10⁻⁶); `gender_Male` no resulta discriminativa.
- **Numéricas (información mutua, estimador KSG):** el rango va de 0 a 0.382. Lidera `GlcCer(d18:1/24:0)` con MI = 0.382. La variable clínica `fit_ug_g` alcanza MI = 0.170, posicionándose en el top 30.
- **Composición del top 20:** dominio de glicerofosfolípidos (9 variables, varias de cadena éter), seguido por esfingolípidos (5), triglicéridos (4) y ésteres de colesterol (2) — diversidad estructural que sugiere que la señal discriminativa no reside en una familia única.

### Caracterización de la dificultad del problema

- En PCA, las elipses de confianza al 95% de las tres clases se superponen casi completamente; CTRL y AA son visualmente indistinguibles en los dos primeros componentes (42.8% de varianza explicada acumulada). La señal biológica existe pero no emerge en los ejes no supervisados de máxima varianza.
- La correlación intra-familia es aproximadamente cinco veces superior a la inter-familia (mediana |r| de 0.43 vs 0.09), con 166 pares por encima de |r| > 0.8: multicolinealidad sustancial que orientará la elección del modelo en el Avance 2.

### Aporte diferencial al estudio original

- **Auditoría metodológica formal** del preprocesamiento (Box-Cox seleccionado tras comparación cuantitativa contra raw, log1p y Yeo-Johnson; imputación validada con norma de Frobenius sobre matrices de correlación; outliers gestionados con la regla IQR sobre datos transformados).
- **Selección supervisada de variables** orientada al problema multiclase CTRL/AA/CRC con un ranking unificado de variables clínicas categóricas (χ²) y numéricas (información mutua), no restringido a comparaciones por pares.
- **Atributos estructurales agregados** (longitud media de cadena, índice de insaturación, fracción de plasmalógenos), evaluados con la misma vara supervisada que el resto del ranking. Su MI individual resulta modesto (≤ 0.021); su valor potencial reside en la interacción con otras variables durante el modelado, aspecto que se evaluará en el Avance 2.

---

## Próximos pasos

El presente entregable corresponde al Avance 1 (Análisis Exploratorio de Datos). Los avances subsecuentes contemplarán:

1. **Construcción del clasificador supervisado multiclase** (CTRL/AA/CRC) sobre las variables seleccionadas en el Paso 4, evaluando Logistic Regression con regularización (L2 / Elastic Net), Random Forest y SVM con kernel RBF.
2. **Comparación de pipelines con y sin variables clínicas** (FIT, FOB) para cuantificar el aporte incremental real de la lipidómica respecto al estándar clínico actual.
3. **Validación cruzada estratificada** con reporte de F1-macro, AUC One-vs-Rest, matriz de confusión y recall por clase, dada la asimetría de costos clínicos.
4. **Interpretación robusta a multicolinealidad** mediante importancia por permutación o SHAP, en sustitución de coeficientes ingenuos o `feature_importances_` directos.
5. **Discusión interdisciplinaria** con el equipo biomédico sobre los hallazgos del EDA y los resultados del modelado.

---

## Procedencia del conjunto de datos

El conjunto `BASE DE DATOS CRC PROYECT LABELED(Data Mat).csv` se obtuvo del Supplementary File S1 (`MX_SuppTable.xlsx`, hoja `DataMat`) del artículo:

> Albóniga, O. E., Cubiella, J., Bujanda, L., Aspichueta, P., Blanco, M. E., Lanza, B., Alonso, C., & Falcón-Pérez, J. M. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, *17*(14), 2339. https://doi.org/10.3390/cancers17142339

El artículo y los materiales suplementarios se distribuyen bajo licencia **Creative Commons Attribution 4.0 (CC BY 4.0)**, lo que permite su redistribución con atribución apropiada.

---

## Referencias metodológicas

- Albóniga, O. E. et al. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, *17*(14), 2339.
- Box, G. E. P., & Cox, D. R. (1964). An analysis of transformations. *Journal of the Royal Statistical Society: Series B*, *26*(2), 211–252.
- Brownlee, J. (2020). *How to choose a feature selection method for machine learning*. Machine Learning Mastery.
- Galli, S. (2022). *Python feature engineering cookbook* (2.ª ed.). Packt Publishing.
- Huang, C. Y., & Dai, H. L. (2021). Learning from class-imbalanced data: Review of data driven methods and algorithm driven methods. *Data Science in Finance and Economics*, *1*(1), 26–36.
- Kraskov, A., Stögbauer, H., & Grassberger, P. (2004). Estimating mutual information. *Physical Review E*, *69*(6), 066138.
- Pearson, K. (1900). On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling. *Philosophical Magazine Series 5*, *50*(302), 157–175.
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, *12*, 2825–2830.

---

## Licencia y uso

Este repositorio constituye trabajo académico desarrollado en el marco del Proyecto Integrador de la Maestría en Inteligencia Artificial Aplicada del Tecnológico de Monterrey. El conjunto de datos y el artículo de referencia se redistribuyen bajo Creative Commons Attribution 4.0. El código y la documentación propia de este repositorio quedan sujetos a uso académico.

---

**Última actualización:** mayo de 2026
