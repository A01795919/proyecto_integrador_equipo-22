---
title: "Hallazgos preliminares del análisis lipidómico CRC"
subtitle: "Memorando para discusión interdisciplinaria con el equipo biomédico"
author:
  - "Sofía Ordaz López"
  - "Equipo de Ciencia de Datos — Proyecto Integrador CRC"
date: "11 de mayo de 2026"
geometry: margin=2.5cm
fontsize: 11pt
linkcolor: blue
header-includes:
  - \usepackage{xcolor}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{Proyecto Integrador CRC}
  - \fancyhead[R]{Hallazgos lipidómicos preliminares}
  - \fancyfoot[C]{\thepage}
---

\vspace{0.5cm}

# Propósito del documento

El presente memorando sintetiza los hallazgos estadísticos derivados del análisis exploratorio del conjunto de datos lipidómico-metabolómico del estudio de cáncer colorrectal en el que colaboramos. Su objetivo no es presentar resultados cerrados sino **abrir un espacio de diálogo interdisciplinario**: las observaciones cuantitativas que se exponen requieren contraste con la interpretación biológica y clínica del equipo biomédico para definir conjuntamente las hipótesis que guiarán la fase de modelado predictivo y la eventual comunicación de resultados.

Cada hallazgo se estructura en tres niveles: **(i)** la observación estadística objetiva, **(ii)** una lectura preliminar tentativa desde la perspectiva de ciencia de datos, y **(iii)** las dimensiones que consideramos especialmente valiosas de discutir desde la perspectiva biológica/clínica.

\vspace{0.4cm}

# 1. Marco analítico

El análisis se realizó sobre 211 muestras fecales (CTRL n=78, AA n=58, CRC n=75) caracterizadas mediante UHPLC-MS, conjunto que coincide íntegramente con el reportado por Albóniga et al. (2025) en *Cancers* 17, 2339. Se aplicó un protocolo de saneamiento estándar (eliminación de 5 lípidos con más del 40% de faltantes), imputación por mediana de grupo, transformación Box-Cox (justificada por su capacidad de normalización: 81% de los lípidos pasan el test de Shapiro-Wilk frente a 5% con Yeo-Johnson y 1% con log), y análisis estadísticos no paramétricos (Kruskal-Wallis, Wilcoxon-Mann-Whitney) con corrección de Benjamini-Hochberg para control de la tasa de falsos descubrimientos.

Como **validación metodológica externa**, el pipeline replicó el 100% de los biomarcadores reportados por Albóniga et al. (7/7 en CRC vs CTRL y 5/5 en CRC vs AA), con la misma dirección y magnitudes consistentes. Esta concordancia respalda la robustez del procedimiento y nos permite presentar con confianza los hallazgos diferenciales que se describen a continuación.

\vspace{0.4cm}

# 2. Hallazgos para discusión conjunta

## 2.1 Patrón de valores faltantes dependiente del grupo

**Observación estadística.** De los 56 lípidos con más del 5% de valores faltantes, 13 (23%) presentan un patrón de ausencia significativamente asociado al grupo clínico (test χ², p < 0.05). El patrón es consistente y direccional: **los faltantes se concentran en CTRL y AA, no en CRC**. Por ejemplo, `SM(36:2)` presenta 53 valores faltantes en CTRL frente a 22 en CRC; `CE(20:5)` muestra 41 faltantes en CTRL frente a 14 en CRC.

**Lectura preliminar.** El patrón es consistente con la hipótesis de que los valores faltantes reflejan concentraciones por debajo del **límite de detección (LOD)** del instrumento UHPLC-MS. Bajo esta interpretación, los faltantes no constituirían ruido aleatorio sino información biológica: indicarían que ciertos lípidos —que se elevan en cáncer colorrectal— se encuentran en niveles muy bajos en individuos sanos y en adenoma, hasta el punto de no ser cuantificables. Esta interpretación motivó nuestra decisión de imputar mediante mediana por grupo (preservando la señal direccional) en lugar de mediana global.

**Aspectos a discutir conjuntamente.** ¿Es plausible que las concentraciones fecales de SM(36:2), CE(20:5), PE(P-18:0/20:4), entre otros, se encuentren rutinariamente por debajo del LOD del instrumento en individuos sanos? ¿La estrategia de imputación que adoptamos resulta razonable desde el punto de vista bioquímico, o existe una alternativa más fiel al fenómeno biológico (por ejemplo, imputación con la mitad del valor mínimo observado)?

## 2.2 Acumulación de ésteres de colesterol en CRC

**Observación estadística.** Cinco ésteres de colesterol presentan incrementos estadísticamente significativos en CRC respecto a CTRL: CE(20:4) (log₂FC = +2.56, q = 7.4×10⁻¹⁰), CE(18:2) (+1.85), CE(20:5) (+1.26), CE(22:6) (+1.06) y CE(18:1) (+0.79). CE(20:4) constituye el biomarcador con mayor poder discriminativo del conjunto, con una concentración mediana aproximadamente seis veces superior en CRC.

**Lectura preliminar.** Albóniga et al. (2025) atribuyen este fenómeno a la vía ACAT1 → PI3K/AKT/mTOR de proliferación tumoral, mecanismo según el cual las células cancerosas reesterifican el colesterol intracelular como reservorio para sostener la síntesis de membranas durante la división celular acelerada. CE(20:4) específicamente transporta ácido araquidónico, precursor de eicosanoides pro-inflamatorios y pro-proliferativos.

**Aspectos a discutir conjuntamente.** ¿La acumulación específica de CEs en muestras **fecales** es coherente con la hipótesis ACAT1, considerando que la materia fecal refleja procesos del lumen intestinal más que del tejido tumoral directamente? ¿Existe una vía alternativa (por ejemplo, exosomas tumorales que liberan CEs al lumen, hipótesis también planteada por Albóniga et al.) que pudiera ser más consistente con la matriz biológica? ¿Cómo se explicaría el patrón observado en CE(20:5) y CE(22:6), que cargan ácidos grasos omega-3 conocidos por su perfil **anti**-inflamatorio?

## 2.3 Elevación de esfingomielinas en CRC

**Observación estadística.** Múltiples esfingomielinas presentan incremento significativo en CRC: SM(d18:1/16:0), SM(d18:1/18:0), SM(d18:1/22:0), SM(d18:1/23:0), SM(d18:1/24:1)+SM(d18:2/24:0), SM(42:1), SM(42:3), SM(33:1), entre otras. El conjunto representa una proporción considerable de los biomarcadores significativos.

**Lectura preliminar.** Las esfingomielinas son componentes estructurales primarios de la membrana celular y los lipid rafts (microdominios de membrana implicados en transducción de señales). Su elevación podría reflejar tanto la mayor producción de membrana asociada a proliferación tumoral como una reestructuración cualitativa de los rafts implicada en señalización oncogénica.

**Aspectos a discutir conjuntamente.** ¿La elevación de SMs es un fenómeno generalizado en CRC documentado en la literatura previa, o constituye un hallazgo específico del estudio Albóniga et al.? ¿Existe especificidad funcional entre las diferentes especies de SMs detectadas (por ejemplo, las saturadas vs las insaturadas)? ¿Es esperable encontrar señal de SMs en matriz fecal, considerando que son lípidos predominantemente intracelulares?

## 2.4 Decremento de triglicéridos específicos en CRC

**Observación estadística.** Varios triglicéridos exhiben el patrón opuesto: descenso estadísticamente significativo en CRC respecto a CTRL. TG(51:4) es el caso más prominente (log₂FC = −1.09, q = 2.3×10⁻⁸), acompañado por TG(54:6), TG(54:7) y un conjunto adicional de TGs poliinsaturados. Es importante destacar que **el decremento de TGs no se observa en AA frente a CTRL** — emerge únicamente al transicionar a la fase de cáncer establecido.

**Lectura preliminar.** Una hipótesis tentativa es que las células tumorales redirigen el metabolismo lipídico hacia la síntesis de membranas (incremento de SMs y CEs ya documentado) a costa de la reserva energética en forma de TGs. Alternativamente, el decremento podría reflejar reducción de absorción intestinal o aumento de β-oxidación.

**Aspectos a discutir conjuntamente.** ¿La reprogramación metabólica desde almacenamiento (TGs) hacia síntesis estructural (SMs, CEs) es un fenómeno documentado en CRC? ¿La especificidad observada en TGs **poliinsaturados** (TG 54:6, TG 54:7) sugiere alguna vía bioquímica particular? ¿El hecho de que el decremento aparezca solo en CRC (no en AA) tiene implicaciones para identificar el momento de transición adenoma → carcinoma?

## 2.5 Glucosilceramidas como hallazgo emergente

**Observación estadística.** En el análisis multivariado mediante PLS-DA, `GlcCer(d18:1/24:0)` emerge como segunda variable con mayor VIP score (2.15) tras CE(20:4); `GlcCer(d18:1/22:0)` también figura en el top 5. Ambas variables son mencionadas como significativas por Albóniga et al. pero **no destacadas como biomarcadores principales** en su discusión.

**Lectura preliminar.** Las glucosilceramidas son precursoras de gangliósidos complejos implicados en señalización y adhesión celular, procesos relevantes en oncogénesis. Su emergencia consistente en nuestro análisis multivariado sugiere que podrían ser biomarcadores subvalorados.

**Aspectos a discutir conjuntamente.** ¿La asociación entre glucosilceramidas y cáncer colorrectal está documentada en la literatura biomédica? ¿Existe alguna razón fisiopatológica para que GlcCer(d18:1/24:0) específicamente —con cadena C24— sea relevante? ¿Convendría priorizar este lípido como candidato a validación adicional?

## 2.6 Fracción de plasmalógenos como marcador potencialmente específico de CRC

**Observación estadística (hallazgo diferencial al paper de referencia).** Construimos un atributo derivado que agrega la fracción de abundancia correspondiente a plasmalógenos (lípidos con prefijo `O-` o `P-`) sobre el total de lípidos por muestra. El comportamiento estadístico de este atributo es notable:

- CRC vs CTRL: p = 0.015 (CRC > CTRL)
- CRC vs AA: p = 0.028 (CRC > AA)
- **AA vs CTRL: p = 0.956 (sin diferencia detectable)**

Es el **único feature analizado donde CRC se separa estadísticamente de ambos grupos restantes y, simultáneamente, AA y CTRL resultan indistinguibles**. Las medianas son CTRL = 0.008, AA = 0.008, CRC = 0.011 (incremento del ~37% en CRC).

**Lectura preliminar.** Los plasmalógenos son antioxidantes naturales de membrana — su enlace vinil-éter en el carbono *sn*-1 actúa como interceptor de especies reactivas de oxígeno. Su elevación específica en CRC podría reflejar una respuesta adaptativa al estrés oxidativo asociado a la progresión tumoral, fenómeno que no se manifiesta aún en la fase de adenoma avanzado.

**Aspectos a discutir conjuntamente.** ¿La hipótesis de plasmalógenos como respuesta adaptativa al estrés oxidativo en cáncer está respaldada por la literatura? Si lo está, el hecho de que el incremento aparezca **únicamente en CRC y no en AA** sería particularmente valioso desde la perspectiva clínica, dado que constituiría un marcador del momento de transición carcinogénica. ¿Sería pertinente proponer este atributo agregado para validación en cohortes independientes?

## 2.7 Naturaleza transicional y heterogénea del adenoma avanzado

**Observación estadística.** La comparación AA vs CTRL revela únicamente **6 lípidos** con diferencias estadísticamente significativas, frente a 38 en CRC vs CTRL y 30 en CRC vs AA. Los únicos lípidos que discriminan AA de CTRL son CE(20:5) (q = 4.7×10⁻⁵), GlcCer(d18:1/24:0), SM(d18:0/18:0), TG(51:4), CE(20:4) (marginal) y PC(36:5). Visualmente, el análisis PCA muestra que la elipse de confianza de AA prácticamente coincide con la de CTRL, con ligera tendencia hacia la elipse de CRC.

**Lectura preliminar.** El adenoma avanzado parece ser una etapa transicional con perfil lipidómico aún cercano al control sano. Solo los CEs (particularmente CE(20:5)) muestran cambios detectables en esta fase, sugiriéndolos como posibles **marcadores tempranos** de progresión hacia cáncer.

**Aspectos a discutir conjuntamente.** ¿La similitud lipidómica entre AA y CTRL es consistente con la observación clínica y patológica? ¿Es plausible que la transición metabólica significativa ocurra en la frontera AA → CRC más que en CTRL → AA? Desde la perspectiva clínica, ¿qué utilidad práctica tendrían biomarcadores capaces únicamente de detectar AA en una fracción de los casos —dado que la señal estadística disponible es escasa— y qué umbrales de sensibilidad/especificidad serían aceptables?

## 2.8 Bimodalidad observada en variables clínicas

**Observación estadística.** Identificamos dos distribuciones bimodales que merecen atención:

- **Edad en CTRL:** la distribución presenta un modo principal en 75–85 años (coincidente con AA y CRC) y un modo secundario menor entre 45 y 55 años. Esto reduce la diferencia real entre las medianas (CTRL 74, AA 78, CRC 79) por debajo de lo que sugieren las medias (CTRL 68.4 vs AA/CRC ~77).
- **FIT en CRC:** distribución claramente bimodal — una pequeña masa en valores bajos y una masa pronunciada en el extremo superior (1001 µg/g, valor de saturación).

**Aspectos a discutir conjuntamente.** ¿Cuál es la justificación de inclusión de los individuos jóvenes (45–55 años) en el grupo CTRL? ¿Corresponden a un perfil clínico específico (por ejemplo, individuos de alto riesgo con colonoscopía preventiva sin hallazgos)? Respecto al FIT bimodal en CRC: ¿la sub-cohorte con FIT bajo corresponde a tumores específicos por localización (proximales/distales), tamaño o estadio? ¿Esta heterogeneidad debe contemplarse en la estrategia de modelado predictivo?

\vspace{0.3cm}

# 3. Implicaciones para la fase de modelado predictivo

La fase subsecuente del proyecto comprende la construcción de un clasificador supervisado para el problema multiclase CTRL/AA/CRC. La interpretación biomédica que el equipo aporte sobre los hallazgos anteriores condicionará varias decisiones de diseño:

1. **Estrategia de imputación.** Si la interpretación LOD es correcta, conviene explorar imputación con valores fijos cercanos al LOD en lugar de mediana por grupo, así como evaluar la inclusión de indicadores binarios de ausencia como predictores.
2. **Selección de variables.** Si las hipótesis sobre glucosilceramidas y plasmalógenos se respaldan biomédicamente, ambos atributos se priorizarán como predictores en el modelo final.
3. **Estrategia de validación clínica.** La heterogeneidad observada (AA transicional, FIT bimodal en CRC) sugiere reportar resultados estratificados además del global, para evidenciar dónde el modelo es clínicamente útil y dónde no.
4. **Marco interpretativo del manuscrito.** Las hipótesis biológicas que se sostengan tras la discusión interdisciplinaria conformarán el discurso del manuscrito final.

\vspace{0.3cm}

# 4. Cierre

Agradecemos al equipo biomédico la dedicación que pueda destinar a la revisión de estos hallazgos. Su perspectiva es complementaria e indispensable: las observaciones estadísticas adquieren sentido únicamente cuando se interpretan en el marco del conocimiento biológico y clínico que ustedes aportan. Quedamos a disposición para profundizar en cualquier punto y para coordinar reuniones de discusión conjunta cuando lo consideren pertinente.

\vspace{0.5cm}

# Referencias

Albóniga, O. E., Cubiella, J., Bujanda, L., Aspichueta, P., Blanco, M. E., Lanza, B., Alonso, C., & Falcón-Pérez, J. M. (2025). Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis. *Cancers*, *17*(14), 2339. https://doi.org/10.3390/cancers17142339

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B (Methodological)*, *57*(1), 289–300.

Box, G. E. P., & Cox, D. R. (1964). An analysis of transformations. *Journal of the Royal Statistical Society: Series B (Methodological)*, *26*(2), 211–252.

Wold, S., Sjöström, M., & Eriksson, L. (2001). PLS-regression: A basic tool of chemometrics. *Chemometrics and Intelligent Laboratory Systems*, *58*(2), 109–130.
