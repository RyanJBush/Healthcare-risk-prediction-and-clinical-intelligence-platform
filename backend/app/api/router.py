from fastapi import APIRouter

from app.routers import explanations, patients, predictions

api_router = APIRouter()
api_router.include_router(patients.router)
api_router.include_router(predictions.router)
api_router.include_router(explanations.router)
