from pydantic import BaseModel, Field

class DiseaseInput(BaseModel):
    crop: str
    growth_stage: str

    vegetation_stress_score: float = Field(ge=0, le=1)
    water_stress_score: float = Field(ge=0, le=1)
    soil_stress_score: float = Field(ge=0, le=1)
    final_stress_percent: float = Field(ge=0, le=100)

    gdd_min: float = Field(ge=0)
    gdd_max: float = Field(ge=0)