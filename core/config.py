from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str = "Crop Disease API"
    VERSION: str = "1.0.0"

    MODEL_PATH_WHEAT: str = "models/wheat/"
    MODEL_PATH_COTTON: str = "models/cotton/"

    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "https://zeocrop.farmseasy.in"
    ]

settings = Settings()