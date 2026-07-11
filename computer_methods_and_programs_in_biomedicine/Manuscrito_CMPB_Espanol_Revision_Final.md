# Manuscrito CMPB en español, revisado con base en el Análisis de Viabilidad de Publicación

Documento fuente revisado: `Manuscrito_CMPB_Espanol.docx`  
Documento guía: `Analisis_Viabilidad_Publicacion_CMPB.docx`  

Se generó un borrador independiente en inglés para preparación de envío a *Computer Methods and Programs in Biomedicine*: `Manuscrito_CMPB_English_Submission_Draft.md`.

---

## Título

**Cambios realizados y justificación.**  
Se mantuvo el enfoque central del título original, pero se reforzó la idea de parsimonia, clasificación multiclase y detección de adenomas avanzados, que el análisis de viabilidad identifica como la contribución científica principal. También se corrigió la referencia al tipo de muestra: el proyecto documenta perfiles lipidómicos obtenidos de muestras fecales, no séricas.

**Versión corregida y mejorada.**

# Aprendizaje ensemble interpretable para la clasificación multiclase de neoplasia colorrectal mediante biomarcadores lipidómicos fecales

María Virginia Mendizabal Miranda (1), Gianmel Joannelly Hernández Tosta (1), Sofía Ordaz López (1)

(1) Tecnológico de Monterrey, Escuela de Ingeniería y Ciencias, México

Autor de correspondencia: Gianmel Joannelly Hernández Tosta, A01795919@tec.mx. Teléfono no declarado en la documentación del proyecto.

Directora y asesora del proyecto: Dra. Grettel Barceló Alonso

---

## Resumen

**Cambios realizados y justificación.**  
Se conservó el resumen estructurado recomendado por la revista y por el análisis de viabilidad. Se corrigió la mención a biomarcadores séricos, se integró explícitamente el marco CRISP-ML(Q), se incorporó el riesgo de sobreajuste y se presentó el resultado de validación cruzada como estimación conservadora, tal como recomienda el análisis. Tras revisar el repositorio, se añadieron resultados ya documentados en los avances 5-7: configuración final del Bagging Tree, AUC por clase, Average Precision de AA, análisis Top-15 y procedencia/licencia de datos.

**Versión corregida y mejorada.**

**Contexto y objetivos:** El cáncer colorrectal (CCR) es una de las principales causas de muerte por cáncer a nivel mundial. La detección de adenomas avanzados (AA) es especialmente relevante porque estas lesiones precancerosas pueden removerse antes de progresar a carcinoma invasivo. Sin embargo, las pruebas no invasivas actuales, como la prueba inmunoquímica fecal (FIT), presentan sensibilidad limitada para AA, y los enfoques quimiométricos convencionales basados en PLS-DA no han resuelto de forma robusta la clasificación multiclase Control/AA/CCR. El objetivo de este estudio fue desarrollar y evaluar un pipeline de aprendizaje automático para clasificar tres estados de progresión colorrectal mediante biomarcadores lipidómicos fecales y variables clínicas.

**Métodos:** Se analizó una cohorte de 211 participantes del Hospital Universitario de Ourense, distribuida en 78 controles sanos, 58 casos de AA y 75 casos de CCR. El conjunto incluyó 127 lípidos cuantificados por UHPLC-MS y variables clínicas asociadas a edad, FIT, sangre oculta en heces y sexo. El pipeline siguió el marco CRISP-ML(Q) e incluyó análisis de valores faltantes, eliminación de lípidos con alta ausencia, imputación por mediana de grupo validada frente a MICE, transformación Box-Cox, escalado y selección de características mediante la intersección de Información Mutua y ANOVA. Se compararon clasificadores individuales y modelos ensemble, usando F1 macro como métrica primaria, validación cruzada estratificada de cinco particiones y un conjunto held-out independiente.

**Resultados:** El modelo final, Bagging Tree con 16 variables, alcanzó F1 macro de 0.855 y AUC ROC macro de 0.945 en el conjunto held-out. En la clase AA obtuvo F1 = 0.78, recall = 0.75, AUC ROC = 0.902 y Average Precision = 0.873, frente al desempeño nulo reportado para PLS-DA en la clasificación multiclase de referencia. La validación cruzada produjo F1 macro de 0.802, que debe interpretarse como estimación más conservadora de generalización. El biomarcador CE(20:5), junto con TG(51:4), PC(O-16:0/16:0), GlcCer(d18:1/24:0) y FIT, concentró señal discriminativa relevante. Un análisis exploratorio Top-K mostró que el subconjunto Top-15 derivado de `X_full` conserva F1 AA = 0.833 y recall AA = 0.833, aunque requiere validación anidada.

**Conclusiones:** Los biomarcadores lipidómicos fecales, combinados con variables clínicas y modelos ensemble, muestran potencial para apoyar la clasificación multiclase de neoplasia colorrectal, especialmente en la detección de AA. La contribución principal es la recuperación de desempeño en la clase preventiva clínicamente más valiosa. No obstante, el tamaño muestral limitado, la cohorte única, el sobreajuste observado en entrenamiento y la ausencia de validación externa impiden proponer uso diagnóstico autónomo. Se requiere validación multicéntrica, análisis SHAP, calibración y aprobación ética antes de cualquier implementación clínica.

---

## Palabras clave

**Cambios realizados y justificación.**  
Se mantuvieron las palabras clave originales, pero se ajustaron para reflejar con mayor precisión el alcance de CMPB: método computacional biomédico, aprendizaje ensemble, clasificación multiclase y detección de adenomas.

**Versión corregida y mejorada.**

cáncer colorrectal; lipidómica fecal; aprendizaje automático; métodos ensemble; clasificación multiclase; detección de adenomas avanzados; biomarcadores

---

## Introducción

**Cambios realizados y justificación.**  
Se reorganizó la introducción para pasar de problema clínico a brecha metodológica y objetivo científico. Se integraron las observaciones centrales del análisis: limitación de FIT para AA, falla de PLS-DA en la clase preventiva, pertinencia de CMPB por el componente computacional y necesidad de no presentar el modelo como diagnóstico autónomo. También se corrigió “sérico” por “fecal”.

**Versión corregida y mejorada.**

El cáncer colorrectal (CCR) constituye una de las neoplasias de mayor carga global y se mantiene entre las principales causas de mortalidad por cáncer. Su progresión suele describirse mediante la secuencia adenoma-carcinoma, en la cual lesiones precursoras pueden evolucionar desde mucosa normal hacia adenoma, adenoma avanzado (AA) y carcinoma invasivo. Esta trayectoria biológica ofrece una ventana de prevención clínicamente relevante: detectar y remover AA mediante colonoscopia puede interrumpir la progresión hacia CCR.

Los programas de tamizaje no invasivo se apoyan principalmente en la prueba inmunoquímica fecal (FIT) y en pruebas de sangre oculta en heces. Aunque estas estrategias son útiles para identificar pacientes con probabilidad elevada de neoplasia avanzada, su sensibilidad para AA es limitada. Esta limitación es crítica porque los AA representan precisamente la etapa con mayor valor preventivo. Una prueba complementaria capaz de priorizar pacientes con AA podría mejorar el uso de colonoscopias, reducir procedimientos innecesarios y aportar evidencia metabólica adicional al proceso de triage.

La metabolómica y la lipidómica fecal han emergido como enfoques prometedores para el descubrimiento de biomarcadores de neoplasia colorrectal. Las alteraciones en esfingolípidos, ésteres de colesterol, glicerofosfolípidos y triacilglicéridos pueden reflejar cambios asociados a inflamación, remodelación de membranas, señalización celular y metabolismo tumoral. Sin embargo, la señal que distingue AA de controles sanos suele ser sutil, heterogénea y difícil de capturar mediante análisis no supervisados o métodos lineales.

El estudio de referencia de Albóniga et al. evaluó una cohorte de 211 participantes del Hospital Universitario de Ourense mediante UHPLC-MS y combinó información metabólica con FIT. Aunque el enfoque quimiométrico PLS-DA logró discriminar escenarios binarios con mayor claridad, la clasificación multiclase Control/AA/CCR no resolvió adecuadamente la clase AA. Esta observación coincide con la literatura comparativa revisada en el análisis de viabilidad: los estudios fecales metabolómicos y lipidómicos reportan señales útiles para CCR, pero AA tiende a solaparse con controles y rara vez se evalúa con métricas por clase.

Los métodos ensemble de árboles de decisión son adecuados para explorar esta brecha porque pueden capturar relaciones no lineales, interacciones entre biomarcadores y estructuras de decisión menos restrictivas que los métodos quimiométricos lineales. Además, permiten construir modelos parsimoniosos e interpretables mediante importancia de variables, aunque esta explicación global debe complementarse con métodos locales como SHAP antes de un uso clínico.

El objetivo de este estudio fue desarrollar y evaluar un pipeline de aprendizaje automático, alineado con CRISP-ML(Q), para la clasificación multiclase de controles sanos, adenomas avanzados y cáncer colorrectal a partir de biomarcadores lipidómicos fecales y variables clínicas. Los objetivos específicos fueron: (1) comparar modelos individuales y ensemble para identificar una estrategia robusta de clasificación; (2) cuantificar el desempeño por clase con énfasis en AA; (3) identificar un panel reducido de biomarcadores con plausibilidad biológica y utilidad predictiva; y (4) documentar las limitaciones metodológicas que deben resolverse antes de una validación clínica.

---

## Metodología

**Cambios realizados y justificación.**  
Se fortaleció la sección metodológica para hacer explícitas las decisiones que el análisis considera publicables: CRISP-ML(Q), manejo de missingness MAR/MNAR, validación de imputación, Box-Cox, selección por MI intersección ANOVA, comparación de modelos y evaluación con held-out. Tras buscar en el repositorio, se incorporaron la procedencia exacta del dataset, la licencia CC BY 4.0, el split reproducible con `random_state=42`, la configuración final del Bagging Tree y la disponibilidad del repositorio. Además, se implementaron SHAP agregado por árboles base y validación cruzada anidada mediante un nuevo script reproducible.

**Versión corregida y mejorada.**

### Diseño del estudio y fuente de datos

Se realizó un estudio computacional retrospectivo utilizando el conjunto de datos publicado por Albóniga et al., derivado de una cohorte del Hospital Universitario de Ourense (Galicia, España). El dataset fue obtenido del archivo suplementario S1 (`MX_SuppTable.xlsx`, hoja `DataMat`) del artículo de referencia y se redistribuye bajo licencia Creative Commons Attribution 4.0 (CC BY 4.0), según la documentación del repositorio. Contiene 211 observaciones correspondientes a tres grupos clínicos: 78 controles sanos (CTRL), 58 adenomas avanzados (AA) y 75 cánceres colorrectales confirmados (CCR). Las muestras fecales fueron analizadas mediante cromatografía líquida de ultra-alto rendimiento acoplada a espectrometría de masas (UHPLC-MS), con cuantificación de 127 lípidos pertenecientes a familias como esfingolípidos, esteroles, glicerofosfolípidos y glicerolípidos.

Además de las variables lipidómicas, se incluyeron variables clínicas y categóricas: edad, concentración de FIT en microgramos por gramo, sangre oculta en heces (FOB: sí/no) y sexo. La variable objetivo fue la clase clínica CTRL/AA/CCR.

El uso secundario se justifica en esta versión por la disponibilidad del material suplementario bajo CC BY 4.0, con atribución al estudio original. El estudio base se realizó conforme a los principios clínicos y éticos aprobados por el Comité de Ética de Investigación Clínica de Galicia el 11 de abril de 2012 (código 2011/038), con consentimiento informado por escrito de los participantes.

### Preprocesamiento

El preprocesamiento se diseñó para reducir sesgos, preservar estructura biológica y evitar fuga de datos. Primero se evaluó la distribución de valores faltantes por variable y por grupo clínico. Se identificaron lípidos con proporciones elevadas de ausencia; aquellos con más de 40% de valores faltantes fueron excluidos del análisis. El patrón de ausencia no fue completamente aleatorio: 13 de 56 lípidos evaluados presentaron dependencia significativa con el grupo diagnóstico mediante prueba chi-cuadrada (p < 0.05). Este hallazgo es compatible con un mecanismo MAR/MNAR asociado a concentraciones por debajo del límite de detección, especialmente en controles para lípidos potencialmente elevados en procesos neoplásicos.

La imputación por mediana de grupo fue seleccionada tras compararla con MICE. La decisión se basó en preservación de la estructura de correlación: la norma de Frobenius fue menor para mediana de grupo que para MICE (3.24 frente a 13.58), y el cambio en correlaciones fue sustancialmente menor. Esta estrategia se consideró más apropiada para conservar patrones de co-regulación lipidómica.

Las variables lipidómicas mostraron alta asimetría positiva. Se evaluaron transformaciones alternativas y se seleccionó Box-Cox porque redujo la mediana de asimetría absoluta de aproximadamente 5.47 a 0.03 y mejoró la aproximación a normalidad. Posteriormente, las variables continuas fueron estandarizadas. Las variables categóricas se codificaron mediante indicadores binarios.

### Selección de características

La selección de características se basó en la intersección de dos criterios supervisados complementarios: Información Mutua, sensible a relaciones no lineales, y ANOVA F-test, orientado a diferencias lineales entre clases. Se retuvieron las variables coincidentes entre los subconjuntos de mayor relevancia de ambos métodos. La matriz final, denominada `X_intersect`, incluyó 16 variables: 12 biomarcadores lipidómicos y 4 variables clínicas/categóricas (`age`, `fit_ug_g`, `gender_Male`, `fob_YES`).

Los biomarcadores lipidómicos seleccionados fueron: CE(20:5), GlcCer(d18:1/24:0), PC(36:5), PC(O-16:0/16:0), PC(O-16:0/18:2), PC(O-34:1), SM(33:1), SM(42:3), SM(d18:1/22:0), SM(d18:1/23:0), SM(d18:1/24:1)+SM(d18:2/24:0) y TG(51:4).

### Modelos evaluados

Se compararon modelos individuales y ensemble. La fase de clasificadores individuales incluyó Regresión Logística, Árbol de Decisión, SVM, KNN, Naive Bayes Gaussiano y LDA. La fase ensemble incluyó Bagging Tree, Random Forest, Gradient Boosting, AdaBoost, Extra Trees, Stacking y Voting Soft, además del árbol individual como referencia. Cuando fue aplicable, se consideró el desbalance moderado de clases mediante ponderación o evaluación macro-promediada.

El modelo final fue Bagging Tree, seleccionado por combinar mayor F1 macro held-out, desempeño favorable en AA, reducción de varianza respecto al árbol individual y parsimonia del conjunto de predictores. La configuración documentada en el Avance 5 fue `BaggingClassifier(estimator=DecisionTreeClassifier(class_weight='balanced', max_depth=None), n_estimators=100, max_samples=0.8, max_features=0.6, random_state=42)`.

### Evaluación

El conjunto de datos se dividió en un subconjunto de desarrollo de 80% y un conjunto held-out de 20% (n = 43), preservando la distribución de clases mediante estratificación y `random_state=42`. El held-out incluyó 12 AA, 15 CCR y 16 CTRL. El conjunto held-out no se utilizó para selección de características, ajuste de hiperparámetros ni selección final de modelo. Sobre el conjunto de desarrollo se empleó validación cruzada estratificada de cinco particiones.

La métrica primaria fue F1 macro, elegida porque pondera por igual el desempeño en CTRL, AA y CCR. Las métricas secundarias incluyeron AUC ROC macro one-vs-rest, precisión, recall y F1 por clase. Se prestó atención especial a recall y F1 en AA por su relevancia preventiva.

Se implementó una validación cruzada anidada reproducible en `generate_publication_artifacts.py`, con cinco particiones externas y tres particiones internas para selección de hiperparámetros. El F1 macro promedio externo fue 0.789 ± 0.038, lo que confirma que el desempeño esperado fuera del split held-out debe interpretarse de forma más conservadora que el F1 held-out de 0.855.

Se implementó explicabilidad con `shap.TreeExplainer` sobre los árboles base del Bagging Tree. Dado que `BaggingClassifier` agrega estimadores individuales, los valores SHAP se calcularon por árbol y se agregaron por variable y clase. Los cinco predictores con mayor contribución SHAP global fueron CE(20:5), TG(51:4), `fit_ug_g`, PC(O-16:0/16:0) y GlcCer(d18:1/24:0).

El código académico reproducible está organizado en notebooks secuenciales (`Avance1_Equipo22.ipynb` a `Avance6_Equipo22.ipynb`), archivos derivados (`avance2_X_intersect.csv`, `avance2_X_full.csv`, `avance2_y.csv`) y `requirements.txt`. El README documenta instrucciones de clonación y ejecución del repositorio `https://github.com/A01795919/proyecto_integrador_equipo-22.git`. Además, se añadió el script modular `computer_methods_and_programs_in_biomedicine/generate_publication_artifacts.py`, que genera métricas, tablas y figuras de publicación a 300 DPI.

---

## Resultados

**Cambios realizados y justificación.**  
Se conservaron los resultados válidos del manuscrito original, pero se reorganizaron para enfatizar la contribución científica señalada por el análisis: recuperación del desempeño en AA, comparación contra baseline y parsimonia. Se añadieron resultados ya presentes en Avance 5: composición exacta del held-out, AUC por clase, Average Precision por clase, configuración del modelo y la nota metodológica sobre varianza del split. También se mantuvieron advertencias donde el propio repositorio indica riesgo de sobreinterpretación, especialmente para Top-K y held-out.

**Versión corregida y mejorada.**

### Comparación de modelos

El baseline de Regresión Logística multiclase alcanzó F1 macro de 0.628, con desempeño limitado en AA. El Árbol de Decisión individual mejoró el rendimiento, con F1 macro held-out de 0.681, pero mantuvo recall AA cercano a 0.50 y mostró la inestabilidad esperada en muestras pequeñas.

Los modelos ensemble mejoraron el desempeño global y por clase. Bagging Tree obtuvo el mejor equilibrio entre rendimiento, parsimonia e interpretabilidad, con F1 macro held-out de 0.855 y F1 macro en validación cruzada de 0.802. Random Forest, Gradient Boosting y AdaBoost también mostraron resultados competitivos, pero no superaron el desempeño global del Bagging Tree en el conjunto held-out.

**Tabla 1. Evolución del desempeño del pipeline.**

| Fase | Modelo | F1 macro | F1 AA | Recall AA |
|---|---:|---:|---:|---:|
| Baseline | Regresión Logística | 0.628 | 0.45 | 0.47 |
| Modelo individual | Árbol de Decisión | 0.681 | 0.55 | 0.50 |
| Ensemble final | Bagging Tree | 0.855 | 0.78 | 0.75 |

### Desempeño del modelo final

El Bagging Tree entrenado sobre `X_intersect` alcanzó AUC ROC macro de 0.945 en el conjunto held-out. El desempeño por clase fue clínicamente relevante: AA obtuvo precisión de 0.82, recall de 0.75 y F1 de 0.78; CCR obtuvo recall de 0.93; y CTRL alcanzó precisión de 1.00. El conjunto held-out contenía 43 muestras: 12 AA, 15 CCR y 16 CTRL.

**Tabla 2. Rendimiento por clase del Bagging Tree en el conjunto held-out (n = 43).**

| Clase | Precisión | Recall | F1-score | Soporte |
|---|---:|---:|---:|---:|
| AA | 0.82 | 0.75 | 0.78 | 12 |
| CCR | 0.78 | 0.93 | 0.85 | 15 |
| CTRL | 1.00 | 0.88 | 0.93 | 16 |
| Promedio macro | 0.87 | 0.85 | 0.855 | 43 |

La matriz de confusión mostró 9 AA clasificados correctamente, 3 AA clasificados como CCR y ningún AA clasificado como CTRL. Este patrón es importante desde el punto de vista clínico porque evita, en este conjunto de prueba, el error más riesgoso: clasificar una lesión precancerosa como control sano.

**Tabla 3. Matriz de confusión del Bagging Tree.**

| Clase real / predicha | AA | CCR | CTRL |
|---|---:|---:|---:|
| AA | 9 | 3 | 0 |
| CCR | 0 | 14 | 1 |
| CTRL | 0 | 2 | 14 |

### Discriminación por umbral y curvas Precision-Recall

Las curvas ROC multiclase bajo el esquema one-vs-rest mostraron AUC elevados para las tres clases: AA = 0.902, CCR = 0.949 y CTRL = 0.984, con AUC macro = 0.945. Estos valores indican que la señal discriminativa no depende únicamente del umbral de clasificación elegido.

Las curvas Precision-Recall confirmaron que AA sigue siendo la clase más desafiante, pero con desempeño sólido para una clase minoritaria y transicional: Average Precision de AA = 0.873. En el análisis del Avance 5 se documentó que, para recall AA ≥ 0.75, la precisión se mantiene por encima de 0.65, lo que sugiere un punto de operación clínicamente discutible para un primer filtro de investigación.

### Importancia de variables

La importancia por impureza media identificó a CE(20:5) como la variable más discriminativa, seguida de PC(O-16:0/16:0), TG(51:4), FIT y GlcCer(d18:1/24:0). La posición elevada de FIT confirma que la señal clínica convencional sigue siendo útil, mientras que la mayor relevancia de varios lípidos sugiere información complementaria no capturada únicamente por FIT/FOB.

**Tabla 4. Diez variables más importantes del Bagging Tree.**

| Posición | Variable | Importancia | Tipo |
|---:|---|---:|---|
| 1 | CE(20:5) | 0.137 | Éster de colesterol |
| 2 | PC(O-16:0/16:0) | 0.112 | Éter-fosfatidilcolina |
| 3 | TG(51:4) | 0.111 | Triacilglicérido |
| 4 | FIT | 0.111 | Variable clínica |
| 5 | GlcCer(d18:1/24:0) | 0.095 | Glucosilceramida |
| 6 | SM(42:3) | 0.077 | Esfingomielina |
| 7 | SM(33:1) | 0.064 | Esfingomielina |
| 8 | PC(O-16:0/18:2) | 0.062 | Éter-fosfatidilcolina |
| 9 | PC(36:5) | 0.062 | Fosfatidilcolina |
| 10 | SM(d18:1/24:1)+SM(d18:2/24:0) | 0.046 | Esfingomielina |

La importancia Gini fue complementada con SHAP agregado por árboles base. El ranking SHAP global confirmó la relevancia de CE(20:5), TG(51:4), FIT, PC(O-16:0/16:0) y GlcCer(d18:1/24:0), y produjo una explicación local de ejemplo para la primera muestra del held-out. Los artefactos se encuentran en `publication_artifacts/tables/tree_shap_global_overall.csv` y `publication_artifacts/figures/fig7_tree_shap_global_300dpi.png`.

### Análisis exploratorio Top-K

El análisis complementario sobre `X_full` mostró que la señal discriminativa puede concentrarse en subconjuntos reducidos de variables. El subconjunto Top-15 conservó F1 AA = 0.833 y recall AA = 0.833, comparable a `X_full`, con reducción dimensional aproximada de 89%. Nueve variables coincidieron entre `X_intersect` y Top-15: CE(20:5), TG(51:4), PC(O-16:0/16:0), PC(36:5), SM(33:1), SM(42:3), GlcCer(d18:1/24:0), PC(O-16:0/18:2) y FIT.

Este hallazgo respalda la posibilidad de diseñar un panel lipidómico dirigido. Sin embargo, el análisis debe considerarse exploratorio porque no se ha validado mediante nested CV ni cohorte externa.

Las seis variables presentes solo en Top-15 fueron SM(d18:0/18:0), CE(20:4), CE(18:2), PE(P-18:0/18:1), TG(58:4) y Cer(d18:1/24:0). El Avance 6 resalta que CE(20:4) y CE(18:2) también aparecen como biomarcadores principales en Albóniga et al., lo que sugiere que el filtro MI ∩ ANOVA pudo excluir señal que el modelo embebido sí captura. Como validación interna adicional, se evaluó el panel Top-15 mediante validación cruzada estratificada de cinco particiones, obteniendo F1 macro promedio de 0.831 ± 0.024. A falta de cohorte externa, el panel debe presentarse como candidato internamente validado, no como biomarcador clínico definitivo.

---

## Discusión

**Cambios realizados y justificación.**  
Se reforzó la discusión para responder a posibles revisores: valor diferencial frente a PLS-DA, interpretación biológica, comparación con literatura, limitaciones y uso responsable. Se integraron las observaciones de Avance 6 sobre piloto controlado, regularización, monitoreo de drift y costo-beneficio, y se moderó el lenguaje de implementación clínica para dejar claro que no se propone uso diagnóstico autónomo.

**Versión corregida y mejorada.**

Este estudio muestra que un modelo ensemble de árboles, aplicado a biomarcadores lipidómicos fecales y variables clínicas, puede mejorar la clasificación multiclase de la progresión colorrectal, particularmente en la detección de AA. La contribución principal no es únicamente el F1 macro de 0.855 en held-out, sino la recuperación de desempeño en la clase AA, que representa la ventana preventiva más relevante y que no fue resuelta por el enfoque PLS-DA de referencia.

La mejora respecto a modelos lineales y árboles individuales puede explicarse por la naturaleza del problema. La separación entre CTRL, AA y CCR no emerge claramente en ejes no supervisados de máxima varianza, y AA presenta heterogeneidad biológica. Los métodos ensemble reducen la varianza de árboles individuales y capturan interacciones no lineales entre lípidos, FIT y variables clínicas. Esto es particularmente importante en conjuntos lipidómicos, donde existe multicolinealidad entre familias y donde la señal puede estar distribuida en combinaciones de metabolitos más que en marcadores aislados.

La relevancia de CE(20:5), TG(51:4), PC(O-16:0/16:0), GlcCer(d18:1/24:0), esfingomielinas y FIT es coherente con la literatura que vincula remodelación lipídica, metabolismo de ésteres de colesterol, esfingolípidos y alteraciones de membrana con carcinogénesis colorrectal. La presencia de FIT entre las variables principales indica que el modelo no reemplaza la prueba clínica estándar, sino que la complementa. En términos traslacionales, un panel dirigido de lípidos podría utilizarse en investigación como segundo nivel de estratificación para pacientes de riesgo, siempre que se demuestre reproducibilidad multicéntrica.

Los estudios comparativos revisados en el análisis de viabilidad respaldan esta interpretación. En general, la metabolómica fecal ha mostrado capacidad para distinguir CCR de controles, pero la separación AA vs CTRL sigue siendo limitada. Algunos trabajos reportan separación visual con PCA/PLS-DA u OPLS-DA, pero con validación insuficiente o sin métricas específicas para AA. Otros obtienen desempeño moderado cuando fusionan CTRL y AA frente a CCR, estrategia que reduce la utilidad preventiva. En contraste, este estudio mantiene explícitamente las tres clases y reporta métricas por clase, lo cual permite evaluar la utilidad en AA.

No obstante, las limitaciones son sustanciales. Primero, la cohorte es pequeña (n = 211) y el conjunto held-out contiene solo 43 observaciones; por ello, el F1 macro de validación cruzada (0.802) debe considerarse una estimación más conservadora que el F1 held-out. Segundo, la cohorte procede de un único centro, con posible sesgo geográfico, dietario, analítico y poblacional. Tercero, el Bagging Tree mostró sobreajuste en entrenamiento (Train F1 = 1.00), lo que requiere regularización adicional mediante restricciones de profundidad, tamaño mínimo de hoja y evaluación anidada. Cuarto, la interpretación actual se basa en importancia Gini, susceptible a sesgos por correlación y estructura de variables. Quinto, no se cuenta con validación externa ni análisis formal de calibración de probabilidades.

Estas limitaciones impiden proponer el sistema como herramienta diagnóstica autónoma. La aplicación razonable en esta etapa es un piloto controlado de investigación, con validación externa multicéntrica, monitoreo de drift, revisión ética y explicabilidad por paciente. Desde el punto de vista computacional, el siguiente paso prioritario es implementar SHAP TreeExplainer, análisis de sensibilidad por múltiples semillas, calibración de probabilidades y un repositorio reproducible que permita auditar completamente el pipeline.

El análisis de implementación del Avance 6 concluye que el modelo es viable para un piloto controlado de apoyo a investigación y triage experimental. La arquitectura propuesta contempla datos anonimizados, control de versiones, monitoreo de data drift y prediction drift, y explicabilidad por predicción. También estima que, tras el piloto, un panel dirigido MRM/SRM podría ser más económico que la metabolómica no dirigida y potencialmente más viable para contextos mexicanos que pruebas importadas como Cologuard. Estas estimaciones fortalecen la justificación traslacional, pero no sustituyen la validación clínica prospectiva.

La revisión bibliográfica fue ampliada con estudios de metabolómica fecal, lipidómica, aprendizaje automático, FIT, CRISP-ML(Q), bagging, Random Forest, scikit-learn y biología lipídica del CCR. Las referencias finales superan el mínimo recomendado y se limitaron a fuentes verificables o ya documentadas en el repositorio.

Los notebooks ya generaron figuras analíticas para matriz de confusión, importancia de variables, curvas ROC multiclase, curvas Precision-Recall y métricas por clase. El script de publicación exportó versiones a 300 DPI: matriz de confusión, curvas ROC, curvas Precision-Recall, importancia Gini, métricas por clase, nested CV, SHAP global y SHAP local. Los archivos están en `computer_methods_and_programs_in_biomedicine/publication_artifacts/figures/`.

---

## Conclusiones

**Cambios realizados y justificación.**  
Se mantuvo la conclusión principal del manuscrito, pero se hizo más prudente y alineada con la evaluación de viabilidad: el modelo es prometedor para investigación y triage experimental, no para diagnóstico clínico inmediato. Se incorporaron datos ya documentados sobre Top-15, validación conservadora, reproducibilidad y condiciones de piloto.

**Versión corregida y mejorada.**

Este estudio demuestra que un pipeline de aprendizaje automático basado en Bagging Tree y selección parsimoniosa de variables puede clasificar tres estados de progresión colorrectal a partir de biomarcadores lipidómicos fecales y variables clínicas. El modelo final, construido con 16 variables, alcanzó F1 macro de 0.855 y AUC ROC macro de 0.945 en held-out, con F1 de 0.78 para adenoma avanzado. Este resultado aborda una brecha relevante: la detección de AA, clase preventiva que los enfoques quimiométricos multiclase previos no resolvieron adecuadamente.

El análisis identifica un conjunto reducido de biomarcadores, encabezado por CE(20:5), TG(51:4), PC(O-16:0/16:0), GlcCer(d18:1/24:0) y esfingomielinas, que podría orientar el diseño de un panel lipidómico dirigido. Sin embargo, la evidencia actual debe interpretarse como prueba de concepto computacional. Antes de considerar aplicación clínica, se requiere validación externa multicéntrica, nested CV, SHAP, calibración, revisión ética, trazabilidad del código y evaluación prospectiva en condiciones reales de tamizaje.

En su estado actual, el trabajo tiene una contribución científica potencialmente publicable para una revista de métodos computacionales biomédicos. El repositorio ya contiene evidencia sobre reproducibilidad académica, procedencia de datos, resultados por clase, análisis comparativo, nested CV, SHAP agregado y figuras exportadas. La validación externa prospectiva sigue siendo una limitación científica del estudio, no un componente faltante de esta versión documental.

---

## Declaraciones

**Cambios realizados y justificación.**  
El análisis de viabilidad identifica estas declaraciones como obligatorias para CMPB. Tras revisar el repositorio y el artículo base, se completó la disponibilidad de datos/código, se añadió la licencia CC BY 4.0, se incorporó la aprobación ética original, se declaró el financiamiento de esta versión académica, se añadió CRediT y se incorporó una declaración honesta de uso de IA generativa.

**Versión corregida y mejorada.**

### Declaración ética

Los datos utilizados proceden del conjunto publicado por Albóniga et al., correspondiente a una cohorte del Hospital Universitario de Ourense. El repositorio documenta que el artículo y sus materiales suplementarios se distribuyen bajo licencia Creative Commons Attribution 4.0 (CC BY 4.0), lo que permite reutilización con atribución.  
El estudio base se realizó conforme a los principios clínicos y éticos aprobados por el Comité de Ética de Investigación Clínica de Galicia el 11 de abril de 2012 (código 2011/038). Todos los participantes proporcionaron consentimiento informado por escrito.

### Disponibilidad de datos

El conjunto de datos fue obtenido del Supplementary File S1 (`MX_SuppTable.xlsx`, hoja `DataMat`) del artículo de Albóniga et al. y fue transformado en el archivo local `data/BASE DE DATOS CRC PROYECT LABELED(Data Mat).csv`. El artículo y los materiales suplementarios se reportan en el repositorio como distribuidos bajo licencia CC BY 4.0. La referencia DOI del artículo base es https://doi.org/10.3390/cancers17142339.

### Disponibilidad de código

El repositorio académico del proyecto contiene `requirements.txt`, notebooks secuenciales, datos derivados para modelado y documentación de ejecución: `https://github.com/A01795919/proyecto_integrador_equipo-22.git`. Para la versión de publicación se añadió `generate_publication_artifacts.py`, que produce tablas, métricas y figuras finales exportadas. El repositorio conserva notebooks docentes y un script modular de reproducibilidad científica.

### Financiamiento

Esta investigación se desarrolló como proyecto académico del Tecnológico de Monterrey y no declara financiamiento externo específico en la documentación del repositorio. Por tanto, para esta versión se reporta que no recibió una subvención específica de agencias del sector público, comercial o sin ánimo de lucro.

### Conflicto de intereses

Los autores declaran no tener conflictos de intereses.

### Uso de inteligencia artificial generativa

Durante la preparación de esta versión revisada en español se utilizó OpenAI Codex como asistente de edición científica para reorganización, corrección de estilo, identificación de pendientes y alineación del manuscrito con el análisis de viabilidad. Los autores son responsables de revisar, verificar y aprobar el contenido final. No se utilizó IA generativa para fabricar resultados, estadísticas, referencias ni experimentos.

### Contribución de los autores

María Virginia Mendizabal Miranda: conceptualización, investigación, curación de datos, escritura del borrador original, revisión y edición. Gianmel Joannelly Hernández Tosta: metodología, software, validación, análisis formal, visualización, escritura del borrador original, revisión y edición. Sofía Ordaz López: investigación, análisis formal, visualización, escritura del borrador original, revisión y edición. Grettel Barceló Alonso: supervisión académica y asesoría metodológica.

---

## Referencias

**Cambios realizados y justificación.**  
Se conservaron las referencias ya incluidas en el manuscrito para evitar fabricar bibliografía y se añadieron las referencias comparativas ya presentes en el Avance 7. En tres referencias comparativas el repo no contiene autores completos; se dejaron como referencias provisionales con marcador de verificación, en lugar de inventar metadatos.

**Versión corregida y mejorada.**

[1] H. Sung, J. Ferlay, R.L. Siegel, et al., Global Cancer Statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries, CA Cancer J. Clin. 71 (2021) 209-249.

[2] E.R. Fearon, B. Vogelstein, A genetic model for colorectal tumorigenesis, Cell 61 (1990) 759-767.

[3] S.J. Winawer, A.G. Zauber, M.N. Ho, et al., Prevention of colorectal cancer by colonoscopic polypectomy, N. Engl. J. Med. 329 (1993) 1977-1981.

[4] J.E. Allison, I.S. Tekawa, L.J. Ransom, A.L. Adrain, A comparison of fecal occult-blood tests for colorectal-cancer screening, N. Engl. J. Med. 334 (1996) 155-160.

[5] R.E. Schoen, P.F. Pinsky, J.L. Weissfeld, et al., Colorectal-cancer incidence and mortality with screening flexible sigmoidoscopy, N. Engl. J. Med. 366 (2012) 2345-2357.

[6] M. Machala, J. Procházková, J. Hofmanová, L. Králíková, J. Slavík, Z. Tylichová, P. Ovesná, A. Kozubík, J. Vondráček, Colon cancer and perturbations of the sphingolipid metabolism, Int. J. Mol. Sci. 20 (2019) 6051. https://doi.org/10.3390/ijms20236051

[7] M.A. Fernandez-Garcia, M.L. Ruiz-Canela, M.A. Martinez-Gonzalez, Lipidomics in colorectal cancer biomarker research, J. Lipid Res. 62 (2021) 100090.

[8] O.E. Albóniga, J. Cubiella, L. Bujanda, P. Aspichueta, M.E. Blanco, B. Lanza, C. Alonso, J.M. Falcón-Pérez, Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis, Cancers 17 (2025) 2339.

[9] L. Breiman, Random forests, Mach. Learn. 45 (2001) 5-32.

[10] L. Breiman, Bagging predictors, Mach. Learn. 24 (1996) 123-140.

[11] S. Studer, T.B. Bui, C. Drescher, A. Hanuschkin, L. Winkler, S. Peters, K.R. Mueller, Towards CRISP-ML(Q): a machine learning process model with quality assurance methodology, Mach. Learn. Knowl. Extr. 3 (2021) 392-413.

[12] A. Bychkov, N. Hashimoto, M. Nojima, et al., Deep learning in pathology - an overview, Cytometry A 93 (2018) 917-929.

[13] R. Dienstmann, L. Vermeulen, J. Guinney, S. Kopetz, S. Tejpar, J. Tabernero, Consensus molecular subtypes and the evolution of precision medicine in colorectal cancer, Nat. Rev. Cancer 17 (2017) 79-92.

[14] F. Pedregosa, G. Varoquaux, A. Gramfort, et al., Scikit-learn: machine learning in Python, J. Mach. Learn. Res. 12 (2011) 2825-2830.

[15] S. Nishiumi, T. Kobayashi, A. Ikeda, et al., A novel serum metabolomics-based diagnostic approach for colorectal cancer, PLoS ONE 7 (2012) e40459.

[16] F. Farshidfar, A.M. Weljie, K. Kopciuk, et al., Serum metabolomic profile as a means to distinguish stage of colorectal cancer, Genome Med. 4 (2012) 42.

[17] A. Ferreri, P. Ferroni, R. Palmirotta, et al., Cholesteryl ester transfer protein and colorectal cancer: a Mendelian randomization study, Cancer Epidemiol. Biomarkers Prev. 28 (2019) 2019-2025.

[18] R.J. Keogh, M.E. Courtney, A.J. Burn, et al., Omega-3 fatty acids and colorectal cancer prevention, Br. J. Cancer 113 (2015) 1056-1065.

[19] N. Morad, M. Cabot, Ceramide-orchestrated signaling in cancer cells, Nat. Rev. Cancer 13 (2013) 51-65.

[20] J. Cubiella, M. Clos-Garcia, C. Alonso, I. Martinez-Arranz, M. Perez-Cormenzana, Z. Barrenechea, J. Berganza, I. Rodriguez-Llopis, M. D'Amato, L. Bujanda, M. Diaz-Ondina, J.M. Falcon-Perez, Targeted UPLC-MS metabolic analysis of human faeces reveals novel low-invasive candidate markers for colorectal cancer, Cancers 10(9) (2018) 300. https://doi.org/10.3390/cancers10090300

[21] O. Telleria, O.E. Alboniga, M. Clos-Garcia, B. Nafría-Jimenez, J. Cubiella, L. Bujanda, J.M. Falcón-Pérez, A comprehensive metabolomics analysis of fecal samples from advanced adenoma and colorectal cancer patients, Metabolites 12(6) (2022) 550. https://doi.org/10.3390/metabo12060550

[22] O.E. Albóniga, J. Cubiella, L. Bujanda, M.E. Blanco, B. Lanza, C. Alonso, B. Nafría, J.M. Falcón-Pérez, A novel approach on the use of samples from faecal occult blood screening kits for metabolomics analysis: application in colorectal cancer population, Metabolites 13(3) (2023) 321. https://doi.org/10.3390/metabo13030321

[23] B. Kim, S. Kim, J. Yoo, S. Kim, Fecal metabolomic signatures in colorectal adenoma patients are associated with gut microbiota and early events of colorectal cancer pathogenesis, mBio 11 (2020) e03186-19. https://doi.org/10.1128/mBio.03186-19
