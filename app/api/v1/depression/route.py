from fastapi import APIRouter
from .schema import DepressionRequest, DepressionResponse
from .service import predict_depression

router = APIRouter()


@router.post("/predict", response_model=DepressionResponse, tags=["Depression"])
async def predict(request: DepressionRequest):
    """
    Predict depression from student data.

    This endpoint evaluates depression risk based on various factors including:
    - Gender and Age
    - Academic pressure and study satisfaction
    - Sleep duration and dietary habits
    - Suicidal thoughts history
    - Study hours and financial stress
    - Family history of mental illness

    Returns:
        - prediction: "Yes" or "No" indicating depression risk
        - probability_depression: Probability score (0-1)
    """
    return predict_depression(request)
