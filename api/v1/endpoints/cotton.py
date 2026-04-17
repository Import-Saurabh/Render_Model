from fastapi import APIRouter
from schemas.disease_schema import DiseaseInput
from services.cotton_service import predict_cotton

router = APIRouter()

@router.post("/predict-diseases")
def predict(data: DiseaseInput):
    result = predict_cotton(data)

    return {
        "crop": data.crop,
        "growth_stage": data.growth_stage,
        "disease_probabilities": result
    }