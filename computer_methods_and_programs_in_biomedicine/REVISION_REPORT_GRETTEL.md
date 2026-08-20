# Revision Report - Dr. Grettel Barceló Alonso

## Changes made

### Introduction

- Strengthened the rationale for colorectal cancer burden, adenoma-carcinoma progression, FIT-based screening, and the need for non-invasive biomarkers.
- Added support for metabolomics/lipidomics in CRC using verified references from the local Albóniga et al. (2025) article and its reference list.
- Corrected the biological sample description from serum/seric to fecal where the manuscript describes the Albóniga et al. dataset.

### Related Work

- Expanded the synthesis of prior metabolomic and lipidomic CRC studies.
- Added literature on serum metabolomics, fecal metabolomics, FIT-kit metabolomics, cholesteryl esters, and advanced colorectal neoplasia.
- Preserved the original research gap, but softened novelty language to avoid unsupported absolute claims.

### Discussion / biological interpretation

- Strengthened the interpretation of CE(20:5), phosphatidylcholines/ether phosphatidylcholines, sphingomyelins, GlcCer, TG(51:4), FIT, and SHAP using conservative biomedical language.
- Clarified that SHAP explains model predictions and does not establish causality, mechanism, or independent clinical validity.
- Clarified that evidence for lipid families does not automatically validate exact molecular species.
- Corrected the PC(O-) discussion so the manuscript does not automatically equate all PC(O-) species with plasmalogens.

### References

- Expanded the bibliography from 21 to 38 references.
- Renumbered in-text citations consistently in Spanish and English.
- Replaced the weak/off-topic Ecker et al. reference with CRC/metabolomics/lipidomics sources more directly relevant to the manuscript.
- Verified added metadata from the locally available Albóniga et al. (2025) PDF and its printed reference list.

### Minor wording corrections

- Softened clinical adoption and population-screening language.
- Replaced economic feasibility claims with language indicating future evaluation.
- Updated selected wording for scientific caution and readability in both Spanish and English.

## New references added

| Reference | Topic | Where cited | Why it was added |
|---|---|---|---|
| Bray et al., 2024 | Global CRC burden | Introduction | Updates global cancer burden support. |
| Brenner and Tao, 2013 | FIT performance | Introduction, Discussion | Supports FIT screening context and limits. |
| Hoseini et al., 2024 | CRC biomarkers | Introduction, Discussion | Adds broad biomarker context. |
| Gold et al., 2022 | CRC metabolomics review | Introduction, Related Work, Discussion | Supports metabolomics/lipidomics rationale. |
| Zhang et al., 2017 | CRC metabolomics systematic review | Introduction, Related Work, Discussion | Supports biomarker discovery context. |
| Ni et al., 2014 | CRC metabonomics | Introduction | Supports early diagnosis/metabolomics rationale. |
| Cubiella et al., 2018 | Fecal UPLC-MS markers | Introduction, Related Work | Directly relevant to fecal CRC metabolomics. |
| Albóniga et al., 2023 | FIT-kit metabolomics | Introduction, Related Work | Directly relevant to non-invasive fecal/FIT samples. |
| Saccenti et al., 2014 | Metabolomics data analysis | Introduction, Related Work | Supports caution around multivariate omics analysis. |
| Wheelock and Wheelock, 2013 | Omics model quality | Introduction, Related Work | Supports cautious interpretation of multivariate models. |
| Nishiumi et al., 2012 | Serum metabolomics CRC diagnosis | Related Work | Prior supervised metabolomics diagnostic study. |
| Farshidfar et al., 2012 | CRC stage metabolomics | Related Work | Prior metabolomics study related to progression. |
| Avram et al., 2025 | Serum metabolites in CRC | Related Work | Adds recent CRC metabolomics evidence. |
| Box and Cox, 1964 | Box-Cox transformation | Methods | Supports the transformation method already described. |
| Fernandez-Garcia et al., 2021 | CRC lipidomics | Discussion | Supports lipidomic interpretation broadly. |
| Liu et al., 2022 | Cholesteryl ester metabolism in CRC | Discussion | Supports CE-family interpretation. |
| Jiang et al., 2024 | Cholesterol metabolism in cancer | Discussion | Supports cholesterol-metabolism context. |
| Goldstein et al., 2006 | Membrane sterol sensors | Discussion | Supports cholesterol homeostasis context. |
| Chang et al., 2009 | ACAT biology | Discussion | Supports cholesterol esterification context. |
| Huang et al., 2020 | Cholesterol metabolism in cancer | Discussion | Supports cancer lipid-metabolism context. |
| Kopecka et al., 2020 | Cholesterol and cancer cells | Discussion | Supports cholesterol-metabolism context. |
| Chen et al., 2018 | ACAT1 in colon cancer | Discussion | Adds CRC-specific cholesterol/ACAT support. |
| Wu et al., 2022 | Cholesterol and CRC growth | Discussion | Adds CRC-specific cholesterol pathway support. |
| Yue et al., 2014 | Cholesteryl ester accumulation in cancer | Discussion | Supports cautious CE interpretation as cancer context. |
| Ye et al., 2016 | ACAT1 in CRC cells | Discussion | Adds CRC-cell evidence for ACAT1 context. |
| Record et al., 2014 | Exosomes and lipid metabolism | Discussion | Supports general vesicular lipid context. |
| Paillasse et al., 2009 | Cholesterol esterification signaling | Discussion | Supports general cholesterol esterification context. |

## Dr. Grettel feedback addressed

| Feedback | Action taken |
|---|---|
| Previous comments still not fully addressed | Strengthened literature support in Introduction, Related Work, and Discussion. |
| SHAP is positive and should remain | SHAP sections, figures, tables, rankings, and numerical values were preserved. Interpretive wording was clarified. |
| Bibliography should be substantially expanded | References increased from 21 to 38 with relevant, verified sources. |
| Biological interpretation needs stronger literature support | Added support for lipid metabolism, cholesteryl esters, phosphatidylcholines, sphingolipids, FIT, and CRC metabolomics/lipidomics. |
| Biomedical statements need careful support | Softened causal/clinical wording and linked biological statements to citations. |
| Supplied papers may help | Used the local Albóniga et al. (2025) PDF and its reference list as the primary source of verified additions. |
| Authorship/domain expertise should be discussed later | Authorship was not changed; this remains for team discussion with Dr. Grettel. |

## Items intentionally not changed

- Methodology was not reanalyzed or redesigned.
- Data analysis, notebooks, datasets, source code, models, preprocessing, SHAP calculations, metrics, and feature rankings were not modified.
- F1 values, AUC values, precision/recall, sample counts, number of variables, hyperparameters, SHAP values, and Top-K results were preserved.
- Figures and tables were not changed.
- Authorship was not changed.

## Remaining items for discussion with Dr. Grettel

- Biomedical-domain expertise/authorship discussion remains unresolved and should be handled by the author team with Dr. Grettel.
- Administrative placeholders remain in both manuscripts for ethics details, repository/data availability, funding, generative AI disclosure, and CRediT author contributions.
- The original ethics approval details are available in the source article, but the manuscript still needs author confirmation on how to state ethics for this secondary analysis.

## Final validation

- Both revised DOCX files are valid ZIP/DOCX packages and can be opened programmatically.
- Both revised manuscripts preserve 10 tables, 5 embedded figures, and 5 image media files.
- Reference numbering was verified: 38 sequential references in both Spanish and English, all cited, with no missing reference entries.
- Main numerical results were checked in the extracted text and preserved.
- Spanish and English versions contain equivalent scientific revisions.
- No new methodology or reanalysis was introduced.
- Visual rendering with the local document renderer could not be completed because the environment lacks the `pdf2image` dependency required by `render_docx.py`; structural validation passed.
