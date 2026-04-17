from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from core.config import settings
from api.v1.endpoints.wheat import router as wheat_router
from api.v1.endpoints.cotton import router as cotton_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wheat_router, prefix="/api/v1/wheat")
app.include_router(cotton_router, prefix="/api/v1/cotton")

@app.get("/")
def root():
    return {"message": "Crop Disease API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Lambda handler
handler = Mangum(app)