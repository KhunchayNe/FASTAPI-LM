from fastapi import APIRouter, File, UploadFile, HTTPException
from .service import predict    

router = APIRouter()


@router.post("/predict", tags=["Animal Image Classification"])
async def getpredict(file: UploadFile = File(...)):

    """
    Predict animal type from an uploaded image.

    This endpoint accepts an image file and returns the predicted animal type.

    Returns:
        - animal_type: Predicted type of the animal in the image
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Here you would add the logic to process the image and make a prediction.
    # For demonstration purposes, we'll return a dummy response.

    return await predict(file)