from pydantic import BaseModel, Field


class DepressionRequest(BaseModel):
    Gender: str
    Age: int = Field(..., ge=10, le=100)

    Academic_Pressure: int = Field(..., ge=0, le=5)
    Study_Satisfaction: int = Field(..., ge=0, le=5)

    Sleep_Duration: str
    Dietary_Habits: str

    Suicidal_Thoughts: str = Field(..., alias="Have you ever had suicidal thoughts ?")

    Study_Hours: int = Field(..., ge=0, le=24)
    Financial_Stress: int = Field(..., ge=0, le=5)

    Family_History: str = Field(..., alias="Family History of Mental Illness")

    class ConfigDict:
        populate_by_name = True


class DepressionResponse(BaseModel):
    prediction: str = Field(..., description="Depression prediction (Yes/No)")
    probability_depression: float = Field(..., description="Probability of depression (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Yes",
                "probability_depression": 0.9965435423302778
            }
        }
