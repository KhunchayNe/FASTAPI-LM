from fastapi import APIRouter
<<<<<<< HEAD
from .service import get_depression
from .schema import DepressionRequest,DepressionUpdate

router = APIRouter()

@router.post('/depression', tags=['Depression'])
def assess_depression(data: DepressionRequest):
    return get_depression()


@router.get('/info', tags=['Depression'])
def info():
    return {"service": "Depression Assessment API", "version": "1.0"}


@router.delete('/depression', tags=['Depression'])
def delete_depression_record(record_id: int):
    return {"status": "deleted", "record_id": record_id}

@router.put('/depression', tags=['Depression'])
def update_depression_record(record_id: int, data: DepressionUpdate):
    return {"status": "updated", "record_id": record_id, "data": data}

@router.patch('/depression', tags=['Depression'])
def partial_update_depression_record(record_id: int, data: dict):
    return {"status": "partially updated", "record_id": record_id, "data": data}
=======
from .schema import DepressionRequest, DepressionResponse
from .service import predict_depression

router = APIRouter()


@router.post("/predict", response_model=DepressionResponse, tags=["Depression Classification"])
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
>>>>>>> origin/dev
