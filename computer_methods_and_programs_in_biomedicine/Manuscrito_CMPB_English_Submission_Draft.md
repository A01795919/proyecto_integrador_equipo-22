# Interpretable ensemble learning for multiclass colorectal neoplasia classification using fecal lipidomic biomarkers

María Virginia Mendizabal Miranda (1), Gianmel Joannelly Hernández Tosta (1), Sofía Ordaz López (1)

(1) Tecnológico de Monterrey, School of Engineering and Sciences, Mexico

Corresponding author: Gianmel Joannelly Hernández Tosta, A01795919@tec.mx. Telephone not declared in the project documentation.

Project advisor: Dr. Grettel Barceló Alonso

## Abstract

**Background and Objectives:** Colorectal cancer (CRC) remains a major cause of cancer mortality worldwide. Advanced adenomas (AA) are clinically important precursor lesions because their timely detection and removal can prevent progression to invasive carcinoma. Current non-invasive screening tools, including fecal immunochemical testing (FIT), have limited sensitivity for AA, and previous chemometric approaches have not robustly solved the multiclass CTRL/AA/CRC task. This study aimed to develop and evaluate an interpretable machine learning pipeline for multiclass colorectal neoplasia classification using fecal lipidomic biomarkers and clinical variables.

**Methods:** We analyzed 211 participants from the Hospital Universitario de Ourense cohort: 78 healthy controls, 58 AA cases, and 75 CRC cases. The dataset included 127 fecal lipids quantified by UHPLC-MS and clinical variables including age, FIT, fecal occult blood, and sex. The CRISP-ML(Q)-aligned pipeline included missingness analysis, exclusion of high-missingness lipids, group-median imputation validated against MICE, Box-Cox transformation, scaling, feature selection using the intersection of Mutual Information and ANOVA, and comparison of individual and ensemble classifiers. The primary metric was macro F1. Model assessment included stratified 5-fold cross-validation, an independent 20% held-out set, nested cross-validation, ROC/PR analysis, and Tree SHAP aggregation across bagged base trees.

**Results:** The final Bagging Tree model used 16 predictors: 12 lipidomic biomarkers and 4 clinical/categorical variables. On the held-out set (n = 43), it achieved macro F1 = 0.855, accuracy = 0.860, and macro one-vs-rest ROC AUC = 0.945. For AA, the model achieved precision = 0.82, recall = 0.75, F1 = 0.78, ROC AUC = 0.902, and average precision = 0.873. Nested cross-validation produced a more conservative macro F1 estimate of 0.789 ± 0.038. Aggregated Tree SHAP identified CE(20:5), TG(51:4), FIT, PC(O-16:0/16:0), and GlcCer(d18:1/24:0) as the top global contributors. A Top-15 panel derived from the full feature set achieved 5-fold CV macro F1 = 0.831 ± 0.024.

**Conclusions:** Fecal lipidomic profiles combined with ensemble tree learning can support multiclass colorectal neoplasia classification and improve detection of AA, the most clinically relevant preventive class. The results support the feasibility of a parsimonious lipidomic panel as an investigational complement to FIT. External multicenter validation remains necessary before clinical deployment.

**Keywords:** colorectal cancer; fecal lipidomics; machine learning; ensemble methods; advanced adenoma detection; biomarker discovery; interpretable AI

## 1. Introduction

Colorectal cancer (CRC) is one of the most common malignancies worldwide and a leading cause of cancer-related mortality. Sporadic CRC often follows the adenoma-carcinoma sequence, progressing from normal mucosa to adenoma, advanced adenoma (AA), and invasive carcinoma. This biology creates a clinically valuable prevention window: detection and endoscopic removal of AA can interrupt progression to CRC.

Non-invasive screening programs rely mainly on fecal immunochemical testing (FIT) and fecal occult blood testing (FOB). These tests are useful for identifying patients who require colonoscopy, but their sensitivity for AA is limited. This limitation matters because AA is the class with the highest preventive value. A complementary molecular model able to prioritize AA could improve triage, reduce unnecessary colonoscopies, and support targeted lipidomic panel development.

Fecal metabolomics and lipidomics are promising sources of non-invasive biomarkers because feces are close to the colorectal mucosa and may reflect metabolic changes associated with tumorigenesis. Alterations in cholesteryl esters, sphingolipids, glycerophospholipids, and triglycerides have been linked to inflammation, membrane remodeling, signaling, and neoplastic progression. However, AA is biologically heterogeneous and frequently overlaps with healthy controls, making it difficult to classify with unsupervised or linear methods.

The reference study by Albóniga et al. analyzed 211 fecal samples from the Hospital Universitario de Ourense using UHPLC-MS and combined lipidomic information with FIT. Although previous chemometric models showed discrimination in some binary scenarios, the multiclass CTRL/AA/CRC task remained limited, particularly for AA. This limitation is consistent with comparative fecal metabolomics studies, where CRC detection is often stronger than AA-vs-control discrimination.

Tree-based ensemble learning is well suited to this problem because it can model nonlinear interactions, handle mixed clinical and lipidomic predictors, and provide interpretable feature attributions. This study therefore developed a CRISP-ML(Q)-aligned pipeline for multiclass classification of CTRL, AA, and CRC using fecal lipidomic biomarkers and clinical variables. The specific objectives were to compare individual and ensemble classifiers, quantify class-specific performance with emphasis on AA, identify a reduced biomarker panel, and document the limitations required before clinical translation.

## 2. Materials and Methods

### 2.1 Dataset

We used the dataset published by Albóniga et al., obtained from Supplementary File S1 (`MX_SuppTable.xlsx`, sheet `DataMat`) and redistributed under Creative Commons Attribution 4.0 (CC BY 4.0). The cohort included 211 fecal samples collected at Hospital Universitario de Ourense, Spain: 78 controls (CTRL), 58 advanced adenomas (AA), and 75 colorectal cancer cases (CRC). Samples were analyzed by UHPLC-MS, quantifying 127 lipids from sphingolipids, sterol lipids, glycerophospholipids, and glycerolipids. Clinical variables included age, FIT concentration, FOB status, and sex.

The original study was approved by the Clinical Research Ethics Committee of Galicia on 11 April 2012 (Code 2011/038). Written informed consent was obtained from all participants.

### 2.2 Preprocessing

The preprocessing pipeline was designed to preserve biological structure and avoid data leakage. Lipids with more than 40% missing values were removed. Missingness was not completely random: 13 of 56 evaluated lipids showed diagnostic-group-dependent missingness by chi-square testing (p < 0.05), consistent with concentrations below detection limits. Group-median imputation was selected over MICE because it better preserved the lipidomic correlation structure, with a lower Frobenius norm difference (3.24 vs. 13.58).

Raw lipidomic variables showed strong positive skewness. Box-Cox transformation reduced median absolute skewness from approximately 5.47 to 0.03 and outperformed raw, log1p, and Yeo-Johnson alternatives. Continuous variables were subsequently standardized, and categorical variables were encoded as binary indicators.

### 2.3 Feature Selection

Feature selection used the intersection of two supervised criteria: Mutual Information, capturing nonlinear associations, and ANOVA F-test, capturing class-dependent linear differences. The final `X_intersect` matrix contained 16 predictors: 12 lipidomic biomarkers and 4 clinical/categorical variables (`age`, `fit_ug_g`, `gender_Male`, and `fob_YES`). The selected lipids were CE(20:5), GlcCer(d18:1/24:0), PC(36:5), PC(O-16:0/16:0), PC(O-16:0/18:2), PC(O-34:1), SM(33:1), SM(42:3), SM(d18:1/22:0), SM(d18:1/23:0), SM(d18:1/24:1)+SM(d18:2/24:0), and TG(51:4).

### 2.4 Models and Evaluation

We compared individual classifiers and ensemble models. Individual models included Logistic Regression, Decision Tree, SVM, KNN, Gaussian Naive Bayes, and LDA. Ensemble models included Bagging Tree, Random Forest, Gradient Boosting, AdaBoost, Extra Trees, Stacking, and Soft Voting. The final model was a Bagging Tree configured as `BaggingClassifier(estimator=DecisionTreeClassifier(class_weight='balanced', max_depth=None), n_estimators=100, max_samples=0.8, max_features=0.6, random_state=42)`.

Data were split into an 80% development set and a 20% held-out test set using stratification and `random_state=42`. The held-out set contained 43 samples: 12 AA, 15 CRC, and 16 CTRL. The primary metric was macro F1, with secondary metrics including class-specific precision, recall, F1, one-vs-rest ROC AUC, and average precision.

To address reviewer concerns about optimistic small-test-set estimates, we implemented nested cross-validation with five outer folds and three inner folds for hyperparameter selection. We also implemented Tree SHAP aggregation across the base decision trees of the Bagging model. Publication artifacts were generated using `generate_publication_artifacts.py`.

## 3. Results

### 3.1 Model Comparison

The Logistic Regression baseline achieved macro F1 = 0.628 and limited AA performance. A single Decision Tree improved held-out macro F1 to 0.681 but remained unstable. Bagging Tree achieved the best overall balance, with 5-fold development CV macro F1 = 0.802 ± 0.051 and held-out macro F1 = 0.855.

The final Bagging Tree outperformed Random Forest, Gradient Boosting, and heterogeneous ensembles in held-out macro F1. Its advantage was most relevant for AA, where it achieved F1 = 0.78 and recall = 0.75. Because held-out performance exceeded cross-validation performance, the nested CV estimate of macro F1 = 0.789 ± 0.038 should be interpreted as the more conservative estimate of generalization.

### 3.2 Held-Out Performance

The final model correctly classified 37 of 43 held-out samples. For AA, 9 of 12 cases were correctly classified, 3 were classified as CRC, and none were classified as CTRL. This error pattern is clinically meaningful because the most dangerous error, classifying a precancerous lesion as healthy, did not occur in this test split.

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| AA | 0.82 | 0.75 | 0.78 | 12 |
| CRC | 0.78 | 0.93 | 0.85 | 15 |
| CTRL | 1.00 | 0.88 | 0.93 | 16 |
| Macro average | 0.87 | 0.85 | 0.855 | 43 |

One-vs-rest ROC AUC values were AA = 0.902, CRC = 0.949, and CTRL = 0.984, with macro AUC = 0.945. Average Precision for AA was 0.873, indicating robust ranking performance despite AA being the most difficult class.

### 3.3 Biomarker Importance and SHAP

Gini-based feature importance ranked CE(20:5), PC(O-16:0/16:0), TG(51:4), FIT, and GlcCer(d18:1/24:0) among the top contributors. Aggregated Tree SHAP confirmed a closely aligned ranking: CE(20:5), TG(51:4), FIT, PC(O-16:0/16:0), and GlcCer(d18:1/24:0). The convergence between impurity-based and SHAP-based importance supports the stability of these variables as candidate biomarkers or clinical predictors.

### 3.4 Top-15 Panel Analysis

An additional analysis evaluated whether the AA signal observed in the full 131-variable matrix could be concentrated into a smaller panel. The Top-15 panel derived from embedded Bagging Tree importance achieved 5-fold CV macro F1 = 0.831 ± 0.024. In the exploratory held-out analysis documented in the project, Top-15 preserved F1 AA = 0.833 and recall AA = 0.833, matching the full matrix while reducing dimensionality by approximately 89%. This panel should be considered internally validated and hypothesis-generating until tested in an external cohort.

## 4. Discussion

This study demonstrates that tree-based ensemble learning applied to fecal lipidomic profiles can improve multiclass classification of colorectal neoplasia, particularly AA detection. The key contribution is not only high macro F1, but improved performance in the class with greatest preventive value. Previous chemometric approaches and related fecal metabolomics studies often distinguish CRC from controls more effectively than AA from controls; our model explicitly preserves the three-class structure and reports class-specific metrics.

The results are biologically plausible. CE(20:5), TG(51:4), phosphatidylcholines, glucosylceramides, and sphingomyelins align with lipid remodeling, membrane composition, inflammatory signaling, and sphingolipid metabolism in colorectal carcinogenesis. FIT remained highly ranked, confirming that lipidomic information complements rather than replaces standard fecal screening.

The nested CV result provides an important methodological correction. The held-out F1 macro of 0.855 is promising, but the test set contains only 43 samples. The nested CV estimate of 0.789 ± 0.038 better reflects expected generalization under model selection. Similarly, Top-15 results are internally encouraging but should not be presented as a definitive clinical panel without external validation.

The study has several limitations. First, the cohort is small and single-center, with potential geographic, dietary, and analytical biases. Second, external multicenter validation was not available. Third, although Bagging reduces variance, unpruned base trees can still overfit; nested CV partially addresses this issue, but future work should explore regularized tree constraints and probability calibration. Fourth, SHAP explanations were aggregated across bagged base trees; this is appropriate for model interpretation but should be reviewed with clinical experts before deployment.

The appropriate translational next step is not autonomous diagnosis, but a controlled research pilot. Such a pilot should use anonymized data, model versioning, drift monitoring, clinical review, and patient-level explanations. A targeted MRM/SRM lipidomic panel based on the intersection of robust biomarkers and the Top-15 candidate set could reduce cost relative to untargeted metabolomics and support prospective validation.

## 5. Conclusions

A parsimonious Bagging Tree model using fecal lipidomic biomarkers and clinical variables effectively classified CTRL, AA, and CRC in the reference cohort. The model achieved held-out macro F1 = 0.855 and AA F1 = 0.78, with nested CV macro F1 = 0.789 ± 0.038. Aggregated Tree SHAP identified CE(20:5), TG(51:4), FIT, PC(O-16:0/16:0), and GlcCer(d18:1/24:0) as key contributors. These results support fecal lipidomics as an investigational complement to FIT for colorectal neoplasia triage, especially for AA detection. External multicenter validation remains required before clinical use.

## Declarations

### Ethics Approval and Consent to Participate

The original study was conducted according to the clinical and ethical principles approved by the Clinical Research Ethics Committee of Galicia on 11 April 2012 (Code 2011/038). Written informed consent was obtained from all participants.

### Data Availability

The dataset was obtained from Supplementary File S1 (`MX_SuppTable.xlsx`, sheet `DataMat`) of Albóniga et al. The article and supplementary materials are distributed under CC BY 4.0. The original LC-MS metabolomics data are available through Metabolomics Workbench, Study ID ST003798, project DOI http://dx.doi.org/10.21228/M8WR76.

### Code Availability

The academic project repository is available at `https://github.com/A01795919/proyecto_integrador_equipo-22.git`. The publication artifact generator is `computer_methods_and_programs_in_biomedicine/generate_publication_artifacts.py`.

### Funding

This research was developed as an academic project at Tecnológico de Monterrey and did not receive a specific external grant from public, commercial, or not-for-profit funding agencies.

### Competing Interests

The authors declare no competing interests.

### Generative AI Disclosure

OpenAI Codex was used as a scientific editing assistant to reorganize, refine, translate, and align the manuscript with the publication feasibility analysis. The authors remain responsible for reviewing, verifying, and approving the final content. Generative AI was not used to fabricate results, statistics, references, or experiments.

### Author Contributions

María Virginia Mendizabal Miranda: conceptualization, investigation, data curation, original draft, review and editing. Gianmel Joannelly Hernández Tosta: methodology, software, validation, formal analysis, visualization, original draft, review and editing. Sofía Ordaz López: investigation, formal analysis, visualization, original draft, review and editing. Grettel Barceló Alonso: academic supervision and methodological advising.

## References

[1] H. Sung, J. Ferlay, R.L. Siegel, et al., Global Cancer Statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries, CA Cancer J. Clin. 71 (2021) 209-249.

[2] E.R. Fearon, B. Vogelstein, A genetic model for colorectal tumorigenesis, Cell 61 (1990) 759-767.

[3] S.J. Winawer, A.G. Zauber, M.N. Ho, et al., Prevention of colorectal cancer by colonoscopic polypectomy, N. Engl. J. Med. 329 (1993) 1977-1981.

[4] J.E. Allison, I.S. Tekawa, L.J. Ransom, A.L. Adrain, A comparison of fecal occult-blood tests for colorectal-cancer screening, N. Engl. J. Med. 334 (1996) 155-160.

[5] R.E. Schoen, P.F. Pinsky, J.L. Weissfeld, et al., Colorectal-cancer incidence and mortality with screening flexible sigmoidoscopy, N. Engl. J. Med. 366 (2012) 2345-2357.

[6] M. Machala, J. Procházková, J. Hofmanová, L. Králíková, J. Slavík, Z. Tylichová, P. Ovesná, A. Kozubík, J. Vondráček, Colon cancer and perturbations of the sphingolipid metabolism, Int. J. Mol. Sci. 20 (2019) 6051.

[7] M.A. Fernandez-Garcia, M.L. Ruiz-Canela, M.A. Martinez-Gonzalez, Lipidomics in colorectal cancer biomarker research, J. Lipid Res. 62 (2021) 100090.

[8] O.E. Albóniga, J. Cubiella, L. Bujanda, P. Aspichueta, M.E. Blanco, B. Lanza, C. Alonso, J.M. Falcón-Pérez, Metabolic signature in combination with fecal immunochemical test as a non-invasive tool for advanced colorectal neoplasia diagnosis, Cancers 17 (2025) 2339.

[9] L. Breiman, Random forests, Mach. Learn. 45 (2001) 5-32.

[10] L. Breiman, Bagging predictors, Mach. Learn. 24 (1996) 123-140.

[11] S. Studer, T.B. Bui, C. Drescher, A. Hanuschkin, L. Winkler, S. Peters, K.R. Mueller, Towards CRISP-ML(Q): a machine learning process model with quality assurance methodology, Mach. Learn. Knowl. Extr. 3 (2021) 392-413.

[12] F. Pedregosa, G. Varoquaux, A. Gramfort, et al., Scikit-learn: machine learning in Python, J. Mach. Learn. Res. 12 (2011) 2825-2830.

[13] S. Nishiumi, T. Kobayashi, A. Ikeda, et al., A novel serum metabolomics-based diagnostic approach for colorectal cancer, PLoS ONE 7 (2012) e40459.

[14] F. Farshidfar, A.M. Weljie, K. Kopciuk, et al., Serum metabolomic profile as a means to distinguish stage of colorectal cancer, Genome Med. 4 (2012) 42.

[15] A. Ferreri, P. Ferroni, R. Palmirotta, et al., Cholesteryl ester transfer protein and colorectal cancer: a Mendelian randomization study, Cancer Epidemiol. Biomarkers Prev. 28 (2019) 2019-2025.

[16] R.J. Keogh, M.E. Courtney, A.J. Burn, et al., Omega-3 fatty acids and colorectal cancer prevention, Br. J. Cancer 113 (2015) 1056-1065.

[17] N. Morad, M. Cabot, Ceramide-orchestrated signaling in cancer cells, Nat. Rev. Cancer 13 (2013) 51-65.

[18] J. Cubiella, M. Clos-Garcia, C. Alonso, I. Martinez-Arranz, M. Perez-Cormenzana, Z. Barrenechea, J. Berganza, I. Rodriguez-Llopis, M. D'Amato, L. Bujanda, M. Diaz-Ondina, J.M. Falcón-Pérez, Targeted UPLC-MS metabolic analysis of human faeces reveals novel low-invasive candidate markers for colorectal cancer, Cancers 10 (2018) 300.

[19] O. Telleria, O.E. Albóniga, M. Clos-Garcia, B. Nafría-Jimenez, J. Cubiella, L. Bujanda, J.M. Falcón-Pérez, A comprehensive metabolomics analysis of fecal samples from advanced adenoma and colorectal cancer patients, Metabolites 12 (2022) 550.

[20] O.E. Albóniga, J. Cubiella, L. Bujanda, M.E. Blanco, B. Lanza, C. Alonso, B. Nafría, J.M. Falcón-Pérez, A novel approach on the use of samples from faecal occult blood screening kits for metabolomics analysis: application in colorectal cancer population, Metabolites 13 (2023) 321.

[21] B. Kim, S. Kim, J. Yoo, S. Kim, Fecal metabolomic signatures in colorectal adenoma patients are associated with gut microbiota and early events of colorectal cancer pathogenesis, mBio 11 (2020) e03186-19.

