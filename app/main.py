import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import app_router
from .core import logger

# Configure logging is handled by core.logger module

app = FastAPI(
    title="AI Prediction Service",
    version="1.0.0",
    description="A service that provides AI-based predictions via RESTful API.",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(app_router, prefix="/api/v1")
