# Avance 7. Resumen ejecutivo

**Equipo 22**  
Maria Virginia Mendizabal Miranda - A01796588  
Gianmel Joannelly Hernandez Tosta - A01795919  
Sofia Ordaz Lopez - A01173717  

**Proyecto:** Analisis de la contribucion de biomarcadores lipidomicos y metabolomicos en modelos de machine learning para cancer colorrectal.  
**Fecha:** Junio de 2026  
**Entregable:** Avance7.Equipo22

## 1. Sintesis ejecutiva

El cancer colorrectal (CRC) es una de las principales causas de muerte por cancer a nivel mundial. La oportunidad clinica mas valiosa no consiste solo en identificar cancer confirmado, sino en detectar adenoma avanzado (AA), lesion precursora que puede removerse mediante colonoscopia antes de progresar a CRC. El proyecto evaluo si perfiles lipidomicos y metabolomicos fecales, combinados con variables clinicas, contienen senal suficiente para clasificar tres estados: control sano (CTRL), adenoma avanzado (AA) y cancer colorrectal (CRC).

La propuesta final es un modelo supervisado multiclase basado en Bagging Tree, entrenado sobre una matriz parsimoniosa de 16 variables: 12 biomarcadores lipidomicos y 4 variables clinicas/categoricas (`age`, `fit_ug_g`, `gender_Male`, `fob_YES`). El modelo alcanzo F1 macro de 0.855 en el conjunto held-out, AUC macro de 0.945 y F1 para AA de 0.78. Este resultado supera el baseline de Regresion Logistica (F1 macro = 0.628), el arbol individual (F1 held-out = 0.681), el antecedente multiclase PLS-DA reportado en el estudio original y los estudios comparativos revisados, donde AA vs control no se evalua o no se discrimina con claridad.

La recomendacion no es desplegar el sistema como diagnostico clinico autonomo. La recomendacion es implementar un piloto controlado de apoyo a investigacion y triage experimental, con validacion externa multicentrica, explicabilidad por paciente, monitoreo de drift y revision etica. Bajo supuestos conservadores, el piloto tiene costos directos estimados de MXN 665,000 para 12 meses de validacion y operacion inicial, con beneficios potenciales de MXN 1.0 a 2.6 millones anuales en eficiencia operativa si se aplica a 1,000 pacientes de tamizaje de alto riesgo, ademas de beneficios intangibles relevantes en prevencion, trazabilidad y aprendizaje clinico.

## 2. Sintesis del problema

El problema de negocio y salud publica es mejorar la deteccion temprana de lesiones colorrectales relevantes, especialmente AA. Las pruebas no invasivas actuales, como FIT/FOB, son utiles para tamizaje, pero presentan sensibilidad limitada para adenomas avanzados. En el dataset de referencia, el propio estudio de Albóniga et al. (2025) reporta que el modelo multiclase PLS-DA con FIT y esteres de colesterol no logra clasificar AA: la clase de mayor valor preventivo se colapsa.

El conjunto de datos utilizado contiene 211 observaciones de la cohorte del Hospital Universitario de Ourense, con tres grupos clinicos: CTRL = 78, AA = 58 y CRC = 75. Incluye variables clinicas y 127 lipidos medidos por UHPLC-MS. La pregunta central fue: puede un modelo de machine learning, con preprocesamiento riguroso y seleccion de biomarcadores, discriminar los tres estados de progresion de CRC mejor que los enfoques previos y sin depender exclusivamente de FIT?

El valor de resolver este problema es doble. En el plano clinico, detectar AA abre una ventana de prevencion antes del cancer invasivo. En el plano operativo, un modelo de triage podria priorizar colonoscopias, orientar paneles lipidomicos dirigidos y generar evidencia para estudios multicentricos posteriores.

## 3. Comentarios y analisis de papers comparativos

Por indicacion de la Dra. Grettel, Aldo Ibanez realizo una busqueda bibliografica en Scopus para ubicar articulos comparables al paper base. El material compartido incluye cuatro articulos originales de los ultimos ocho anos con enfoque similar: metabolomica/lipidomica en muestras fecales para distinguir CRC, adenoma/adenoma avanzado y controles sanos. La conclusion transversal del analisis comparativo es importante para este proyecto: los estudios respaldan el valor de metabolitos fecales para detectar CRC, pero ninguno resuelve de forma robusta la discriminacion AA vs controles sanos.

| Articulo comparativo | Muestra | Metodos principales | Resultado clave | AA vs CTRL |
|---|---|---|---|---|
| Metabolomic analysis of gut metabolites in patients (Oncology Letters, 2023) | 35 CRC, 37 CRA, 30 controles sanos | UHPLC-MS/MS, PCA, OPLS-DA, prueba de permutacion, analisis univariado, ROC y supervivencia global | Detecto 1641 metabolitos; reporto metabolitos asociados a CRC vs controles y CRA vs controles | No |
| A novel approach on the use of samples from faecal occult blood screening kits for metabolomics analysis (Metabolites, 2023) | Tres lotes: CTL, AD y CRC; total con predominio de CTL/AD y pocos CRC en lote 3 | CV%, PCA, PLS-DA, OPLS-DA, ANOVA, t-test/Mann-Whitney | PLS-DA/OPLS-DA separaron visualmente, pero no pasaron criterios de validacion; diferencias significativas solo CTL vs CRC o AD vs CRC | No; CTL y AD no tuvieron diferencias suficientes |
| A comprehensive metabolomics analysis of fecal samples from advanced adenoma and colorectal cancer patients (Metabolites, 2022) | 40 controles, 40 AA, 40 CRC | UHPLC-MS/MS, PCA, Random Forest, Regresion Logistica, k-fold CV y LOOCV | RF multiclase obtuvo 52% de exactitud; CTL y AA se confundieron con frecuencia; fusion CTL+AA vs CRC alcanzo 75% | No |
| Targeted UPLC-MS metabolic analysis of human faeces reveals novel low-invasive candidate markers for colorectal cancer (Cancers, 2018) | 40 AA, 40 CRC, 49 controles | UPLC-MS, ANOVA, PCA, PLS-DA, Regresion Logistica y ROC | ChoE y FOB mejoraron la discriminacion de CRC; siete metabolitos mas FOB alcanzaron AUC mediana de 0.885 | No |

El benchmark externo refuerza tres comentarios ejecutivos. Primero, la metabolomica fecal es una via biologicamente plausible y metodologicamente consistente: los cuatro estudios usan espectrometria de masas y reportan senales en esfingolipidos, esteres de colesterol, trigliceridos, hemoglobina fecal u otros metabolitos. Segundo, la literatura converge en una dificultad especifica: AA tiende a parecerse mas a controles que a CRC, por lo que los enfoques no supervisados (PCA/PLS-DA) o las comparaciones binarias tienden a ocultar justamente la clase preventiva mas importante. Tercero, nuestro proyecto aporta una mejora diferencial porque formula el problema como clasificacion multiclase desde el inicio, reporta metricas por clase y logra F1 AA = 0.78 con Bagging Tree, en lugar de colapsar AA con controles o con CRC.

Estos papers tambien ayudan a interpretar los biomarcadores seleccionados. La aparicion repetida de familias como ChoE/CE, SM y TG en la literatura es coherente con variables relevantes de nuestro modelo, como `CE(20:5)`, `TG(51:4)`, `SM(d18:0/18:0)` y `PC(O-16:0/16:0)`. Por tanto, el modelo no solo mejora el desempeno tecnico; tambien mantiene continuidad biologica con hallazgos previos.

## 4. Hallazgos principales del EDA

El analisis exploratorio confirmo que el dataset es pequeno pero informativo. La distribucion de clases tiene desbalance leve: CTRL 37.0%, CRC 35.5% y AA 27.5%, por lo que Macro F1 fue elegida como metrica principal para no ocultar el desempeno de AA.

La calidad de datos requirio decisiones explicitas. Se identificaron 27 lipidos con mas de 20% de valores faltantes y 5 con mas de 40%, que fueron eliminados. El mecanismo de ausencia no fue aleatorio: 13 de 56 lipidos evaluados tuvieron missingness dependiente del grupo (chi-cuadrada, p < 0.05). Este patron es compatible con concentraciones por debajo del limite de deteccion, mas frecuentes en controles para ciertos lipidos elevados en CRC. Por ello se eligio imputacion por mediana de grupo y se valido contra MICE. La mediana de grupo preservo mejor la estructura de correlacion (norma de Frobenius 3.24 vs 13.58).

Las distribuciones lipidomicas presentaban alta asimetria. Box-Cox fue la transformacion seleccionada porque redujo la mediana de skewness absoluta de aproximadamente 5.47 a 0.03. Despues de transformar, se detectaron 769 outliers sobre 25,742 celdas (2.99%), una tasa razonable para mediciones biologicas.

En el analisis multivariado, PCA mostro superposicion sustancial entre CTRL, AA y CRC, lo que indica que la senal no aparece en los ejes no supervisados de maxima varianza. En contraste, la seleccion supervisada si identifico biomarcadores discriminativos. `fob_YES` fue una variable categorica altamente informativa (chi-cuadrada = 23.9), mientras que entre las numericas destacaron lipidos como `GlcCer(d18:1/24:0)`, `CE(20:5)`, `TG(51:4)` y `PC(O-16:0/16:0)`. Tambien se observo multicolinealidad relevante: la correlacion intra-familia fue aproximadamente cinco veces mayor que la inter-familia, por lo que la parsimonia de features se volvio una decision critica.

## 5. Modelos generados y eleccion del modelo final

La evolucion de modelos siguio la logica CRISP-ML(Q): baseline interpretable, modelo individual y ensamble. Primero se entreno Regresion Logistica multiclase sobre `X_intersect`, obteniendo F1 macro de 0.628, F1 para AA de 0.38 y recall AA de 0.47. Este baseline mostro viabilidad predictiva, pero tambien revelo que AA era la clase dificil.

Despues se evaluo un Decision Tree individual. El arbol mejoro el F1 macro a 0.707 en validacion cruzada y 0.681 en held-out, con recall AA cercano a 0.50. Este modelo aporto interpretabilidad, pero presento alta varianza e inestabilidad esperada en datasets pequenos.

Finalmente se evaluaron modelos ensemble. El modelo seleccionado fue Bagging Tree sobre `X_intersect`, con 100 arboles agregados por bootstrap. Fue elegido porque redujo la varianza del arbol individual, mantuvo interpretabilidad razonable mediante importancia de variables y obtuvo el mejor equilibrio entre desempeno, parsimonia y utilidad clinica. Sus resultados principales fueron:

| Metrica | Resultado |
|---|---:|
| F1 macro held-out | 0.855 |
| F1 macro CV | 0.802 |
| AUC ROC macro | 0.945 |
| F1 AA | 0.78 |
| Recall AA | 0.75 |
| Recall CRC | 0.93 |
| Precision CTRL | 1.00 |
| Numero de features | 16 |

### 5.1 Visualizacion ejecutiva de hallazgos

La figura sintetiza el hallazgo mas importante para un tomador de decisiones: la clase AA, que es la ventana preventiva del proceso clinico, pasa de no estar resuelta en el benchmark multiclase previo a obtener desempeno util con el modelo final. En este grafico, la escala se interpreta como F1 para AA cuando esta disponible; para Top 15 se reporta el valor exploratorio observado en held-out.

[[CHART:AA_DETECTION]]

La eleccion de `X_intersect` se justifica porque concentra senal robusta bajo dos criterios independientes: Mutual Information y ANOVA. Tambien evita el riesgo de sobreajuste asociado con `X_full` (131 variables). Como analisis complementario, `X_full Top 15` con Bagging Tree conservo Recall AA = 0.833 y F1 AA = 0.833, por lo que queda como candidato para validacion futura, pero no reemplaza al modelo final hasta completar nested CV y validacion externa.

### 5.2 Comparativa entre X_intersect y X_full Top 15

A solicitud de la Dra. Grettel se listaron lado a lado los predictores de ambos subconjuntos. La coincidencia es del 60% (9 de 15 variables comunes), lo que confirma una senal robusta entre dos estrategias de seleccion independientes (filtro supervisado MI cap ANOVA y seleccion embebida por importancia del Bagging Tree).

| Categoria | Variables |
|---|---|
| Comunes a X_intersect y Top 15 (9) | CE(20:5), TG(51:4), PC(O-16:0/16:0), PC(36:5), SM(33:1), SM(42:3), GlcCer(d18:1/24:0), PC(O-16:0/18:2), fit_ug_g |
| Solo en X_intersect (7) | PC(O-34:1), SM(d18:1/22:0), SM(d18:1/23:0), SM(d18:1/24:1)+SM(d18:2/24:0), age, gender_Male, fob_YES |
| Solo en Top 15 (6) | SM(d18:0/18:0), CE(20:4), CE(18:2), PE(P-18:0/18:1), TG(58:4), Cer(d18:1/24:0) |

Las 6 variables nuevas en Top 15 incluyen dos biomarcadores reportados como principales en el paper de Alboniga et al. (2025): CE(20:4) y CE(18:2). Su ausencia en X_intersect indica que el filtro MI cap ANOVA del Avance 2 perdio senal que el modelo embedded si captura. Este hallazgo refuerza la propuesta de panel lipidomico dirigido descrita en la seccion 6 y abre la posibilidad de un panel ampliado a aproximadamente 15 lipidos sin sacrificar interpretabilidad.

## 6. Recomendaciones clave de implementacion

La implementacion debe realizarse como piloto controlado, no como herramienta diagnostica autonoma. El objetivo del piloto es validar integracion tecnica, estabilidad del pipeline y utilidad para priorizacion experimental.

Las acciones prioritarias son:

| Recomendacion | Responsable | Entregable esperado | Prioridad |
|---|---|---|---|
| Validar el modelo con cohorte externa independiente, idealmente n >= 200 y multicentrica | Patrocinador academico y equipo clinico | Reporte de metricas externas vs internas | Alta |
| Regularizar Bagging Tree (`max_depth=7-10`, `min_samples_leaf=3-5`) | Equipo de ciencia de datos | Modelo con brecha train-CV menor a 0.10 | Alta |
| Generar explicabilidad SHAP por paciente | Equipo ML y equipo clinico | Reporte interpretativo por prediccion | Alta |
| Disenar panel lipidomico reducido basado en Top 15 | Laboratorio de espectrometria y equipo ML | Lista de biomarcadores y protocolo MRM/SRM | Alta |
| Aprobar protocolo etico y consentimiento informado | Comite de etica | Protocolo aprobado | Alta |
| Implementar prototipo en Google Vertex AI | Equipo tecnico/MLOps | Endpoint, monitoreo y dashboard interno | Media-alta |
| Monitorear data drift, prediction drift y tasa de deteccion AA | Equipo MLOps | Alertas y reporte mensual | Alta |

Google Vertex AI se recomienda como plataforma inicial por su continuidad con notebooks, pipelines reproducibles, Model Registry, monitoreo de drift y capacidad de escalar hacia validacion multicentrica. AWS SageMaker y Azure ML son alternativas viables si el hospital ya opera con esos ecosistemas.

## 7. Analisis costo-beneficio

### 7.1 Supuestos de planeacion

Las cifras siguientes son estimaciones para presentar a stakeholders y deben refinarse con cotizaciones institucionales. Se usa MXN como moneda de planeacion. Para servicios cloud internacionales y panel lipidomico se asumen paridades internas de referencia de 1 USD = MXN 20 y 1 EUR = MXN 22 (junio 2026). El costo de hora tecnica se estima en MXN 350 para trabajo academico/prototipo. El costo de metabolomica no dirigida se estima en MXN 10,000-11,000 por muestra (aprox. EUR 500) y el panel dirigido MRM/SRM en MXN 1,100-2,200 por muestra (aprox. EUR 50-100), conforme a los rangos refinados en el Avance 6 tras la retroalimentacion docente.

### 7.2 Costos incurridos por fase CRISP-ML(Q)

| Fase CRISP-ML(Q) | Concepto | Supuesto | Costo estimado |
|---|---|---:|---:|
| Business & Data Understanding | Adquisicion de datos y articulo base | Dataset y paper bajo acceso abierto/CC BY 4.0 | MXN 0 |
| Business & Data Understanding | Revision bibliografica y definicion del problema | 24 h tecnicas | MXN 8,400 |
| Data Preparation | Limpieza, reconstruccion de encabezados, imputacion, Box-Cox | 60 h tecnicas | MXN 21,000 |
| Data Preparation | Computo local y almacenamiento | Laptop existente, sin hardware dedicado | MXN 0 |
| Modeling | Entrenamiento de baseline, arbol, ensembles y seleccion de features | 45 h tecnicas | MXN 15,750 |
| Evaluation | Validacion cruzada, held-out, analisis Top-K y metricas por clase | 35 h tecnicas | MXN 12,250 |
| Deployment planning | Arquitectura cloud, recomendaciones y documentacion | 30 h tecnicas | MXN 10,500 |
| Documentation | Integracion de avances y reporte ejecutivo | 25 h tecnicas | MXN 8,750 |
| Servidores/cloud usados hasta la fecha | Ejecucion local/notebooks; sin endpoint persistente | Costo incremental minimo | MXN 0 |
| Software | Python, scikit-learn, pandas, Jupyter, Git | Open source | MXN 0 |
| **Total incurrido estimado** |  | 219 h tecnicas | **MXN 76,650** |

### 7.3 Costos esperados de operacion y mantenimiento

Se plantea un piloto de 12 meses con 200 muestras externas para validacion y uso controlado sobre 1,000 predicciones de triage experimental.

| Componente | Supuesto | Costo anual estimado |
|---|---:|---:|
| Panel lipidomico dirigido para validacion externa | 200 muestras x MXN 1,850 | MXN 370,000 |
| Preparacion y control de calidad de datos externos | 80 h tecnicas | MXN 28,000 |
| Ajuste/regularizacion y nested CV | 60 h tecnicas | MXN 21,000 |
| SHAP, reporte clinico e interpretabilidad | 50 h tecnicas | MXN 17,500 |
| Cloud Vertex AI Workbench/Pipelines/Registry | MXN 3,500 mensuales | MXN 42,000 |
| Endpoint online y batch prediction | MXN 2,800 mensuales | MXN 33,600 |
| Monitoreo de drift y auditoria mensual | 10 h/mes | MXN 42,000 |
| Seguridad, documentacion etica y trazabilidad | 60 h tecnicas | MXN 21,000 |
| Mantenimiento correctivo/evolutivo | 8 h/mes | MXN 33,600 |
| Reserva de contingencia | 10% del subtotal | MXN 56,970 |
| **Total operacion + validacion 12 meses** |  | **MXN 665,670** |

Si el modelo pasa a uso rutinario posterior al piloto, el costo recurrente sin validacion externa intensiva bajaria aproximadamente a MXN 150,000-220,000 anuales, mas el costo variable de muestras lipidomicas procesadas.

### 7.4 Beneficios cuantificables

Los beneficios se estiman para una cohorte anual de 1,000 pacientes en tamizaje de alto riesgo o derivados por sospecha clinica. No se asume que el modelo sustituya la colonoscopia; se asume que mejora priorizacion y reduce procedimientos innecesarios una vez validado.

| Beneficio | Supuesto conservador | Valor anual estimado |
|---|---|---:|
| Reduccion de colonoscopias innecesarias en controles | Evitar 10% de colonoscopias en pacientes de bajo riesgo; 70 procedimientos x MXN 8,000 | MXN 560,000 |
| Priorizacion temprana de AA | 40 AA adicionales priorizados antes; ahorro operativo y clinico proxy de MXN 12,000 por caso | MXN 480,000 |
| Sustitucion parcial de metabolomica no dirigida por panel dirigido | 200 muestras: ahorro de MXN 7,400 por muestra | MXN 1,480,000 |
| Reduccion de retrabajo analitico y revision manual | 120 h clinico-tecnicas x MXN 500 | MXN 60,000 |
| **Beneficio anual potencial bruto** | Escenario con panel dirigido y triage validado | **MXN 2,580,000** |

En un escenario prudente, aplicando solo 40% de captura efectiva por incertidumbre de adopcion, el beneficio anual seria MXN 1,032,000. Comparado con el costo anual del piloto (MXN 665,670), el retorno potencial seria positivo (beneficio/costo aproximado de 1.55). En un escenario completo, el beneficio/costo podria acercarse a 3.9. Estas cifras no deben interpretarse como ROI clinico definitivo, sino como racional economico para financiar la validacion.

**Posicionamiento competitivo frente a Cologuard (alternativa de EE.UU.):** El test de ADN en heces Cologuard de Exact Sciences, la alternativa no invasiva mas conocida en Estados Unidos, cuesta entre MXN 10,000 y MXN 15,000 por test e implica importacion desde EE.UU. El panel lipidomico dirigido propuesto en este proyecto cuesta entre MXN 1,100 y MXN 2,200 por muestra: es entre 5 y 10 veces mas barato y puede producirse localmente en laboratorios mexicanos con espectrometros de masas dirigidos. Para sistemas de salud publicos con presupuesto limitado (IMSS, ISSSTE), esto representa una via economicamente viable para escalamiento poblacional que Cologuard no permite.

**Ahorro estimado por paciente FIT-positivo:** El protocolo de tamizaje actual cuesta aproximadamente MXN 10,500 por paciente con FIT positivo (FIT ~MXN 500 mas colonoscopia ~MXN 10,000). Bajo el protocolo propuesto (FIT mas panel lipidomico como filtro, con colonoscopia solo cuando ambos resultan positivos), el ahorro estimado seria de MXN 3,000 a MXN 5,000 por paciente FIT-positivo, dependiendo de la tasa de filtrado del panel (escenario conservador 30%, escenario optimista 50% basado en la precision CTRL = 1.00 del modelo). Este ahorro por paciente es complementario al beneficio agregado de la tabla anterior y refuerza la viabilidad operativa del piloto.

### 7.5 Beneficios intangibles

El proyecto aporta beneficios cualitativos importantes. Primero, transforma mediciones lipidomicas complejas en una herramienta interpretable para investigacion clinica. Segundo, mejora la trazabilidad de decisiones mediante CRISP-ML(Q), versionamiento del pipeline y monitoreo. Tercero, permite generar hipotesis biologicas sobre biomarcadores como `CE(20:5)`, `TG(51:4)` y `PC(O-16:0/16:0)`. Cuarto, ayuda a construir capacidades institucionales de MLOps responsable en salud. Finalmente, enfoca la atencion en AA, clase que representa la ventana preventiva mas valiosa.

## 8. Riesgos y desafios de la solucion

La clasificacion de riesgos sigue cuatro categorias solicitadas en los recursos de la semana: datos, ataques, prueba y confianza, y cumplimiento.

| Categoria | Riesgo | Impacto | Mitigacion |
|---|---|---|---|
| Datos | Cohorte unica de Ourense y n pequeno (211 muestras) | Sobreestimacion del desempeno y baja generalizacion | Validacion externa multicentrica con n >= 200 antes de uso clinico |
| Datos | Missingness MAR/MNAR por limite de deteccion | Sesgo si se imputa de forma global o se ignora la ausencia informativa | Mantener imputacion validada, indicadores de ausencia y auditoria por grupo |
| Datos | Drift por cambios en protocolo UHPLC-MS o poblacion | Degradacion silenciosa del modelo | Monitoreo de data drift y recalibracion documentada |
| Datos | Multicolinealidad lipidomica | Importancias inestables y explicaciones fragiles | Seleccion parsimoniosa, SHAP con cautela y validacion biologica |
| Ataques | Acceso no autorizado a datos de salud | Riesgo de privacidad y dano reputacional | Anonimizacion, IAM, cifrado, bitacoras y minimo privilegio |
| Ataques | Envenenamiento de datos en reentrenamiento | Modelo sesgado o inseguro | Reentrenamiento solo con cohortes aprobadas y revision de calidad |
| Ataques | Manipulacion de entrada o uso fuera de contexto | Predicciones no confiables | Validaciones de schema, rangos biologicos y alertas de anomalia |
| Prueba y confianza | Sobreajuste del Bagging Tree (Train F1 = 1.00) | Desempeno menor en poblaciones nuevas | Regularizacion, nested CV y evaluacion externa |
| Prueba y confianza | Varianza del held-out pequeno (n = 43) | Confianza excesiva en F1 = 0.855 | Reportar F1 CV = 0.802 como estimacion conservadora |
| Prueba y confianza | AA es biologicamente heterogeneo | Falsos negativos en la clase preventiva clave | Optimizar umbrales por clase y estudiar subtipos de AA |
| Prueba y confianza | Explicabilidad insuficiente para adopcion clinica | Baja confianza del usuario | SHAP por paciente y revision con especialistas |
| Cumplimiento | Uso como dispositivo medico sin validacion | Riesgo regulatorio y etico | Limitar el piloto a investigacion; no usar como diagnostico autonomo |
| Cumplimiento | Consentimiento y uso secundario de datos lipidomicos | Incumplimiento etico/legal | Protocolo aprobado por comite de etica y consentimiento explicito |
| Cumplimiento | Transferencia internacional o cloud de datos sensibles | Riesgo normativo | Datos anonimizados, region cloud definida, DPA/BAA si aplica |
| Cumplimiento | Sesgo por poblacion no representativa | Inequidad en desempeno | Reporte estratificado por sexo, edad, centro y subpoblacion |

## 9. Cierre ejecutivo

El proyecto demuestra que existe senal lipidomica util para clasificar CTRL, AA y CRC, y que un ensemble de arboles con seleccion parsimoniosa de biomarcadores supera claramente los modelos previos evaluados. La contribucion central no es solo el F1 macro de 0.855, sino la recuperacion de desempeno en AA, clase que el antecedente multiclase no lograba detectar.

La decision ejecutiva recomendada es financiar un piloto controlado de 12 meses. El costo estimado de MXN 665,670 es razonable frente a beneficios potenciales conservadores de MXN 1.0 millones anuales y frente al valor clinico de priorizar lesiones precancerosas. La condicion indispensable es mantener el sistema como apoyo experimental hasta completar validacion externa, explicabilidad, monitoreo, aprobacion etica y analisis de cumplimiento.

## 10. Referencias

Albóniga, O. E., Cubiella, J., Bujanda, L., Aspichueta, P., Blanco, M. E., Lanza, B., Alonso, C., & Falcón-Pérez, J. M. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, 17(14), 2339. https://doi.org/10.3390/cancers17142339

Baccarin, F. (2020). Machine learning that pays the bills: choosing models in business contexts. *Towards Data Science*. https://towardsdatascience.com/machine-learning-that-pays-the-bills-choosing-models-in-business-contexts-e9003fd434a1

Babic, B., Cohen, I. G., Evgeniou, T., & Gerke, S. (2021). When machine learning goes off the rails. *Harvard Business Review*. https://hbr.org/2021/01/when-machine-learning-goes-off-the-rails

Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24(2), 123-140. https://doi.org/10.1007/BF00058655

Cubiella, J., Clos-Garcia, M., Alonso, C., Martinez-Arranz, I., Perez-Cormenzana, M., Barrenechea, Z., Berganza, J., Rodriguez-Llopis, I., D'Amato, M., Bujanda, L., Diaz-Ondina, M., & Falcon-Perez, J. M. (2018). Targeted UPLC-MS metabolic analysis of human faeces reveals novel low-invasive candidate markers for colorectal cancer. *Cancers*, 10(9), 300. https://doi.org/10.3390/cancers10090300

Metabolites. (2022). A comprehensive metabolomics analysis of fecal samples from advanced adenoma and colorectal cancer patients. *Metabolites*, 12(6), 550.

Metabolites. (2023). A novel approach on the use of samples from faecal occult blood screening kits for metabolomics analysis: application in colorectal cancer population. *Metabolites*, 13(3), 321.

Oncology Letters. (2023). Metabolomic analysis of gut metabolites in patients. *Oncology Letters*, 26(2).

Studer, S., Bui, T. B., Drescher, C., Hanuschkin, A., Winkler, L., Peters, S., & Müller, K. R. (2021). Towards CRISP-ML(Q): A machine learning process model with quality assurance methodology. *Machine Learning and Knowledge Extraction*, 3(2), 392-413. https://doi.org/10.3390/make3020020
