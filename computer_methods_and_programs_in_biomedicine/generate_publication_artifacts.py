"""Generate publication-ready evaluation artifacts for the CMPB manuscript.

The script consumes the matrices exported in Avance 2 and reproduces the final
Bagging Tree evaluation with additional nested CV, SHAP-style TreeExplainer
aggregation over the bagged base trees, and 300 DPI figures.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(SCRIPT_DIR / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parents[1]
OUT = SCRIPT_DIR / "publication_artifacts"
FIG = OUT / "figures"
TAB = OUT / "tables"
RANDOM_STATE = 42
LABELS = ["AA", "CRC", "CTRL"]


def final_bagging(**overrides) -> BaggingClassifier:
    params = dict(
        estimator=DecisionTreeClassifier(class_weight="balanced", max_depth=None, random_state=RANDOM_STATE),
        n_estimators=100,
        max_samples=0.8,
        max_features=0.6,
        random_state=RANDOM_STATE,
        n_jobs=1,
    )
    params.update(overrides)
    return BaggingClassifier(**params)


def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=300, bbox_inches="tight")
    plt.close()


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    x_intersect = pd.read_csv(ROOT / "notebooks" / "avance2_X_intersect.csv")
    x_full = pd.read_csv(ROOT / "notebooks" / "avance2_X_full.csv")
    y = pd.read_csv(ROOT / "notebooks" / "avance2_y.csv")["group"]
    return x_intersect, x_full, y


def evaluate_final_model(x: pd.DataFrame, y: pd.Series) -> dict:
    x_dev, x_test, y_dev, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    model = final_bagging()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, x_dev, y_dev, cv=cv, scoring="f1_macro", n_jobs=1)
    model.fit(x_dev, y_dev)
    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)
    class_order = list(model.classes_)

    report = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True, zero_division=0)).T
    report.to_csv(TAB / "final_model_classification_report.csv")

    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    pd.DataFrame(cm, index=[f"real_{c}" for c in LABELS], columns=[f"pred_{c}" for c in LABELS]).to_csv(
        TAB / "final_model_confusion_matrix.csv"
    )
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS)
    disp.plot(cmap="Blues", colorbar=False)
    plt.title("Bagging Tree: matriz de confusion held-out")
    savefig("fig1_confusion_matrix_300dpi.png")

    y_bin = LabelBinarizer().fit_transform(y_test)
    bin_classes = list(LabelBinarizer().fit(LABELS).classes_)
    proba_df = pd.DataFrame(y_proba, columns=class_order)
    roc_rows = []
    pr_rows = []
    plt.figure(figsize=(6.2, 4.6))
    for cls_idx, cls in enumerate(bin_classes):
        y_true = (y_test.to_numpy() == cls).astype(int)
        scores = proba_df[cls].to_numpy()
        fpr, tpr, _ = roc_curve(y_true, scores)
        auc_value = roc_auc_score(y_true, scores)
        roc_rows.append({"class": cls, "roc_auc": auc_value})
        plt.plot(fpr, tpr, label=f"{cls} (AUC={auc_value:.3f})")
    plt.plot([0, 1], [0, 1], "--", color="0.5", linewidth=1)
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("Curvas ROC one-vs-rest")
    plt.legend()
    savefig("fig2_multiclass_roc_300dpi.png")

    plt.figure(figsize=(6.2, 4.6))
    for cls in bin_classes:
        y_true = (y_test.to_numpy() == cls).astype(int)
        scores = proba_df[cls].to_numpy()
        precision, recall, _ = precision_recall_curve(y_true, scores)
        ap_value = average_precision_score(y_true, scores)
        pr_rows.append({"class": cls, "average_precision": ap_value})
        plt.plot(recall, precision, label=f"{cls} (AP={ap_value:.3f})")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Curvas Precision-Recall one-vs-rest")
    plt.legend()
    savefig("fig3_precision_recall_300dpi.png")

    pd.DataFrame(roc_rows).to_csv(TAB / "final_model_roc_auc_by_class.csv", index=False)
    pd.DataFrame(pr_rows).to_csv(TAB / "final_model_average_precision_by_class.csv", index=False)

    importances = np.zeros(x.shape[1])
    for estimator, feature_idx in zip(model.estimators_, model.estimators_features_):
        importances[feature_idx] += estimator.feature_importances_
    importances /= len(model.estimators_)
    importance_df = pd.DataFrame({"feature": x.columns, "importance": importances}).sort_values(
        "importance", ascending=False
    )
    importance_df.to_csv(TAB / "final_model_feature_importance.csv", index=False)
    plt.figure(figsize=(7, 5.2))
    top = importance_df.head(15).iloc[::-1]
    plt.barh(top["feature"], top["importance"], color="#2f6f8f")
    plt.xlabel("Importancia Gini agregada")
    plt.title("Top features del Bagging Tree")
    savefig("fig4_feature_importance_300dpi.png")

    metrics = report.loc[LABELS, ["precision", "recall", "f1-score"]].reset_index(names="class")
    metrics_long = metrics.melt(id_vars="class", var_name="metric", value_name="value")
    plt.figure(figsize=(6.2, 4.2))
    sns.barplot(data=metrics_long, x="class", y="value", hue="metric", palette="Set2")
    plt.ylim(0, 1.05)
    plt.title("Metricas por clase en held-out")
    savefig("fig5_class_metrics_300dpi.png")

    macro_auc = roc_auc_score(pd.get_dummies(y_test)[class_order], y_proba, average="macro", multi_class="ovr")
    summary = {
        "heldout_n": int(len(y_test)),
        "heldout_support": y_test.value_counts().sort_index().to_dict(),
        "cv_f1_macro_mean": float(cv_scores.mean()),
        "cv_f1_macro_sd": float(cv_scores.std(ddof=1)),
        "heldout_f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        "heldout_accuracy": float((y_pred == y_test).mean()),
        "heldout_auc_macro_ovr": float(macro_auc),
        "classes": class_order,
    }
    return {"model": model, "x_dev": x_dev, "x_test": x_test, "y_dev": y_dev, "y_test": y_test, "summary": summary}


def run_nested_cv(x: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    param_grid = {
        "n_estimators": [50, 100],
        "max_samples": [0.6, 0.8],
        "max_features": [0.6, 1.0],
        "estimator__max_depth": [None, 7, 10],
        "estimator__min_samples_leaf": [1, 3, 5],
    }
    outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    inner = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)
    rows = []
    for fold, (train_idx, test_idx) in enumerate(outer.split(x, y), start=1):
        search = GridSearchCV(
            final_bagging(),
            param_grid=param_grid,
            scoring="f1_macro",
            cv=inner,
            n_jobs=1,
            refit=True,
        )
        search.fit(x.iloc[train_idx], y.iloc[train_idx])
        pred = search.predict(x.iloc[test_idx])
        rows.append(
            {
                "outer_fold": fold,
                "test_f1_macro": f1_score(y.iloc[test_idx], pred, average="macro"),
                "best_inner_f1_macro": search.best_score_,
                "best_params": json.dumps(search.best_params_, sort_keys=True),
            }
        )
    nested = pd.DataFrame(rows)
    nested.to_csv(TAB / "nested_cv_final_model.csv", index=False)

    plt.figure(figsize=(5.8, 4.2))
    sns.stripplot(data=nested, y="test_f1_macro", color="#315c64", size=8)
    plt.axhline(nested["test_f1_macro"].mean(), color="#b0473c", linestyle="--", label="media")
    plt.ylim(0, 1)
    plt.ylabel("F1 macro")
    plt.title("Nested CV del Bagging Tree final")
    plt.legend()
    savefig("fig6_nested_cv_300dpi.png")
    return nested


def run_top15_validation(x_full: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    top15 = [
        "CE(20:5)",
        "TG(51:4)",
        "PC(O-16:0/16:0)",
        "PC(36:5)",
        "SM(33:1)",
        "SM(42:3)",
        "GlcCer(d18:1/24:0)",
        "PC(O-16:0/18:2)",
        "fit_ug_g",
        "SM(d18:0/18:0)",
        "CE(20:4)",
        "CE(18:2)",
        "PE(P-18:0/18:1)",
        "TG(58:4)",
        "Cer(d18:1/24:0)",
    ]
    missing = [feature for feature in top15 if feature not in x_full.columns]
    if missing:
        raise ValueError(f"Missing Top-15 features in X_full: {missing}")
    x_top = x_full[top15]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    model = final_bagging(n_estimators=200, max_samples=0.6, max_features=1.0)
    scores = cross_val_score(model, x_top, y, cv=cv, scoring="f1_macro", n_jobs=1)
    rows = [{"fold": i + 1, "f1_macro": score} for i, score in enumerate(scores)]
    result = pd.DataFrame(rows)
    result.to_csv(TAB / "top15_cross_validation.csv", index=False)
    pd.DataFrame({"feature": top15}).to_csv(TAB / "top15_features.csv", index=False)
    return result


def run_shap_tree_aggregation(model: BaggingClassifier, x_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    classes = list(model.classes_)
    mean_abs = {cls: np.zeros(x_test.shape[1]) for cls in classes}
    local_predicted_class_values = np.zeros(x_test.shape[1])

    sample_idx = 0
    for estimator, feature_idx in zip(model.estimators_, model.estimators_features_):
        x_subset = x_test.iloc[:, feature_idx]
        explainer = shap.TreeExplainer(estimator)
        values = explainer.shap_values(x_subset)
        if isinstance(values, list):
            class_arrays = values
        else:
            arr = np.asarray(values)
            if arr.ndim == 3:
                class_arrays = [arr[:, :, i] for i in range(arr.shape[2])]
            else:
                class_arrays = [arr]
        for cls_pos, cls in enumerate(estimator.classes_):
            cls_label = classes[int(cls)] if isinstance(cls, (int, np.integer)) else cls
            global_cls_pos = classes.index(cls_label)
            vals = class_arrays[cls_pos]
            mean_abs[classes[global_cls_pos]][feature_idx] += np.abs(vals).mean(axis=0)

        predicted_cls = model.predict(x_test.iloc[[sample_idx]])[0]
        encoded_predicted_cls = classes.index(predicted_cls)
        if encoded_predicted_cls in estimator.classes_:
            cls_pos = list(estimator.classes_).index(encoded_predicted_cls)
            local_predicted_class_values[feature_idx] += class_arrays[cls_pos][sample_idx]

    for cls in classes:
        mean_abs[cls] /= len(model.estimators_)
    local_predicted_class_values /= len(model.estimators_)

    global_rows = []
    for cls in classes:
        for feature, value in zip(x_test.columns, mean_abs[cls]):
            global_rows.append({"class": cls, "feature": feature, "mean_abs_tree_shap": value})
    shap_global = pd.DataFrame(global_rows)
    shap_global.to_csv(TAB / "tree_shap_global_by_class.csv", index=False)

    shap_overall = (
        shap_global.groupby("feature", as_index=False)["mean_abs_tree_shap"].mean().sort_values(
            "mean_abs_tree_shap", ascending=False
        )
    )
    shap_overall.to_csv(TAB / "tree_shap_global_overall.csv", index=False)
    plt.figure(figsize=(7, 5.2))
    top = shap_overall.head(15).iloc[::-1]
    plt.barh(top["feature"], top["mean_abs_tree_shap"], color="#5b7f3a")
    plt.xlabel("Mean |Tree SHAP| agregado")
    plt.title("Importancia global Tree SHAP agregada")
    savefig("fig7_tree_shap_global_300dpi.png")

    local = pd.DataFrame(
        {
            "feature": x_test.columns,
            "tree_shap_value_predicted_class": local_predicted_class_values,
            "sample_value": x_test.iloc[sample_idx].to_numpy(),
        }
    )
    local["abs_value"] = local["tree_shap_value_predicted_class"].abs()
    local = local.sort_values("abs_value", ascending=False)
    local.to_csv(TAB / "tree_shap_local_sample0.csv", index=False)
    plt.figure(figsize=(7, 5.2))
    local_top = local.head(10).iloc[::-1]
    colors = ["#b0473c" if v > 0 else "#315c64" for v in local_top["tree_shap_value_predicted_class"]]
    plt.barh(local_top["feature"], local_top["tree_shap_value_predicted_class"], color=colors)
    plt.axvline(0, color="0.4", linewidth=1)
    plt.xlabel("Tree SHAP para clase predicha")
    plt.title("Explicacion local agregada: muestra held-out 0")
    savefig("fig8_tree_shap_local_300dpi.png")
    return shap_overall


def main() -> None:
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    TAB.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    x_intersect, x_full, y = load_data()
    final = evaluate_final_model(x_intersect, y)
    nested = run_nested_cv(x_intersect, y)
    top15 = run_top15_validation(x_full, y)
    shap_overall = run_shap_tree_aggregation(final["model"], final["x_test"], final["y_test"])

    summary = final["summary"]
    summary.update(
        {
            "nested_cv_f1_macro_mean": float(nested["test_f1_macro"].mean()),
            "nested_cv_f1_macro_sd": float(nested["test_f1_macro"].std(ddof=1)),
            "top15_cv_f1_macro_mean": float(top15["f1_macro"].mean()),
            "top15_cv_f1_macro_sd": float(top15["f1_macro"].std(ddof=1)),
            "top5_tree_shap_features": shap_overall.head(5)["feature"].tolist(),
        }
    )
    (OUT / "summary_metrics.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
