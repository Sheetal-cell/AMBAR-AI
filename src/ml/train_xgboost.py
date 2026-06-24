from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from sqlalchemy import create_engine, text

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    KFold
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

from src.config.settings import settings
from src.utils.logging_utils import logger

DATA_FILE = Path(
    "data/training/aqi_features.parquet"
)

MODEL_DIR = Path(
    "models/xgboost"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH = MODEL_DIR / "aqi_xgb_v1.pkl"

engine = create_engine(
    settings.DATABASE_URL
)


def load_data():
    logger.info("Loading features")

    return pd.read_parquet(
        DATA_FILE
    )


def prepare_xy(df):
    X = df.drop(
        columns=["aqi"]
    )

    y = df["aqi"]

    return X, y


def train_model(X_train, y_train):

    params = {
        "n_estimators": [200, 300, 500],
        "max_depth": [4, 6, 8, 10],
        "learning_rate": [0.01, 0.05, 0.1],
        "subsample": [0.7, 0.8, 1.0],
        "colsample_bytree": [0.7, 0.8, 1.0]
    }

    model = XGBRegressor(
        objective="reg:squarederror",
        random_state=42
    )

    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=params,
        n_iter=20,
        cv=KFold(
            n_splits=5,
            shuffle=True,
            random_state=42
        ),
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
        verbose=2
    )

    search.fit(
        X_train,
        y_train
    )

    return search.best_estimator_


def evaluate(
    model,
    X_test,
    y_test
):
    preds = model.predict(
        X_test
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            preds
        )
    )

    mae = mean_absolute_error(
        y_test,
        preds
    )

    r2 = r2_score(
        y_test,
        preds
    )

    logger.info(
        f"RMSE={rmse:.3f}"
    )

    logger.info(
        f"MAE={mae:.3f}"
    )

    logger.info(
        f"R2={r2:.3f}"
    )

    return rmse, mae, r2


def save_model(model):
    joblib.dump(
        model,
        MODEL_PATH
    )

    logger.info(
        f"Saved model {MODEL_PATH}"
    )


def update_registry(
    rmse,
    mae,
    r2
):
    query = text(
        """
        INSERT INTO model_registry
        (
            model_name,
            version,
            rmse,
            mae,
            r2,
            model_path
        )
        VALUES
        (
            :model_name,
            :version,
            :rmse,
            :mae,
            :r2,
            :model_path
        )
        """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "model_name": "AQI_XGBOOST",
                "version": "v1",
                "rmse": float(rmse),
                "mae": float(mae),
                "r2": float(r2),
                "model_path": str(MODEL_PATH)
            }
        )


def main():

    df = load_data()

    X, y = prepare_xy(df)

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = train_model(
        X_train,
        y_train
    )

    rmse, mae, r2 = evaluate(
        model,
        X_test,
        y_test
    )

    save_model(model)

    update_registry(
        rmse,
        mae,
        r2
    )


if __name__ == "__main__":
    main()