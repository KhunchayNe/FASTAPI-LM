import joblib
import pandas as pd
from pathlib import Path
from .schema import DepressionRequest, DepressionResponse
from loguru import logger
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

MODEL_PATH = (
    Path(__file__).parent.parent.parent.parent / "models" / "depression_model.joblib"
)

# Load model once at module level
artifact = joblib.load(MODEL_PATH)
model_features = artifact["features"]
model = artifact["model"]


def to_df(req: DepressionRequest, features) -> pd.DataFrame:
    row = {
        "Gender": req.Gender,
        "Age": req.Age,
        "Academic Pressure": req.Academic_Pressure,
        "Study Satisfaction": req.Study_Satisfaction,
        "Sleep Duration": req.Sleep_Duration,
        "Dietary Habits": req.Dietary_Habits,
        "Have you ever had suicidal thoughts ?": req.Suicidal_Thoughts,
        "Study Hours": req.Study_Hours,
        "Financial Stress": req.Financial_Stress,
        "Family History of Mental Illness": req.Family_History,
    }

    
   
    return pd.DataFrame([row], columns=features)


def predict_depression(request: DepressionRequest) -> DepressionResponse:
    X = to_df(request, model_features)

    prob = float(model.predict_proba(X)[0][1])
    pred = int(model.predict(X)[0])

    return DepressionResponse(
        prediction="Yes" if pred == 1 else "No",
        probability_depression=prob,
    )
# input_data = {
#     "Gender": request.Gender,
#     "Age": request.Age,
#     "Academic Pressure": request.Academic_Pressure,
#     "Study Satisfaction": request.Study_Satisfaction,
#     "Sleep Duration": request.Sleep_Duration,
#     "Dietary Habits": request.Dietary_Habits,
#     "Have you ever had suicidal thoughts ?": request.Suicidal_Thoughts,
#     "Study Hours": request.Study_Hours,
#     "Financial Stress": request.Financial_Stress,
#     "Family History of Mental Illness": request.Family_History,
# }

# input_df = pd.DataFrame([input_data])

# prediction_proba = model.predict_proba(input_df)[0]
# probability_depression = prediction_proba[1]
# prediction = "Yes" if probability_depression >= 0.5 else "No"

# return DepressionResponse(
#     prediction=prediction,
#     probability_depression=probability_depression
# )
