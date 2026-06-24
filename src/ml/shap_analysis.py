from pathlib import Path

import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt

from src.utils.logging_utils import logger

MODEL_PATH = Path(
    "models/xgboost/aqi_xgb_v1.pkl"
)

DATA_PATH = Path(
    "data/training/aqi_features.parquet"
)

OUTPUT_DIR = Path(
    "models/shap"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_model():
    return joblib.load(
        MODEL_PATH
    )


def load_data():
    df = pd.read_parquet(
        DATA_PATH
    )

    return df.drop(
        columns=["aqi"]
    )


def generate_summary_plot(
    explainer,
    X
):
    shap_values = explainer(
        X
    )

    plt.figure()

    shap.summary_plot(
        shap_values,
        X,
        show=False
    )

    plt.savefig(
        OUTPUT_DIR /
        "summary_plot.png",
        bbox_inches="tight"
    )

    plt.close()

    logger.info(
        "Saved summary plot"
    )


def save_importance(
    explainer,
    X
):
    shap_values = explainer(X)

    importance = pd.DataFrame({
        "feature": X.columns,
        "importance":
            abs(
                shap_values.values
            ).mean(axis=0)
    })

    importance = (
        importance
        .sort_values(
            "importance",
            ascending=False
        )
    )

    importance.to_csv(
        OUTPUT_DIR /
        "feature_importance.csv",
        index=False
    )

    logger.info(
        "Saved SHAP importance"
    )


def main():

    model = load_model()

    X = load_data()

    explainer = shap.Explainer(
        model
    )

    generate_summary_plot(
        explainer,
        X
    )

    save_importance(
        explainer,
        X
    )


if __name__ == "__main__":
    main()