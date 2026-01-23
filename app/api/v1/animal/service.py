import io
import json
from loguru import logger
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import HTTPException, File, UploadFile
from pathlib import Path

MODEL_PATH = (
    Path(__file__).parent.parent.parent.parent / "models" / "animal_cnn_224.keras"
)

LABELS_PATH = (
    Path(__file__).parent.parent.parent.parent / "models" / "labels.json"
)

IMG_SIZE = (224, 224)


with open(LABELS_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)["class_names"]

def load_image2(file_bytes):
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    img = img.resize(IMG_SIZE)
    arr = np.asarray(img, dtype=np.float32)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return np.expand_dims(arr, axis=0)

def load_image(file_bytes): 
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    img = img.resize((224, 224))
    arr = np.asarray(img, dtype=np.float32)   # keep 0..255
    arr = np.expand_dims(arr, axis=0)         # [1,224,224,3]
    return arr


async def predict(file: UploadFile = File(...)):

    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")

    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=415, detail="Unsupported image type")
    
    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
    img_bytes = await file.read()
    x = load_image(img_bytes)

    model = tf.keras.models.load_model(MODEL_PATH)
    logger.info(f"Load model successfully from {MODEL_PATH}")

    probs = model.predict(x)[0]
    idx = int(np.argmax(probs))

    return {
        "prediction": class_names[idx],
        "confidence": float(probs[idx]),
    }