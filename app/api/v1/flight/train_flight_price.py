import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = "app/api/v1/flight/data/flight_dataset.csv"
OUT_DIR = "app/models"
MODEL_PATH = os.path.join(OUT_DIR, "flight_price_model.joblib")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # Target
    y = df["Price"]

    '''
    # Features
    features = [
        "Airline",
        "Source",
        "Destination",
        "Total_Stops",
        "Month",
        "Year",
        "Dep_hours",
        "Dep_min",
        "Arrival_hours",
        "Arrival_min",
        "Duration_hours",
        "Duration_min",
    ]
    '''
    features = [
        "Airline",
        "Source",
        "Destination",
        "Total_Stops",
        "Month",
        "Year",
        "Duration_hours",
        "Duration_min",
    ]



    X = df[features]

    categorical = ["Airline", "Source", "Destination"]
    numeric = [c for c in features if c not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=400,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=2
    )

    pipeline = Pipeline(steps=[
        ("prep", preprocessor),
        ("model", model)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    artifact = {
        "version": "1.0.0",
        "model": pipeline,
        "features": features,
        "mae": float(mae),
        "r2" : r2_score(y_test, preds),
        "rows": len(df),
        "target": "Flight ticket price"
    }

    joblib.dump(artifact, MODEL_PATH)

    print("Model saved to:", MODEL_PATH)
    print("MAE:", mae)
    print("R2", r2_score(y_test, preds))

if __name__ == "__main__":
    main()
