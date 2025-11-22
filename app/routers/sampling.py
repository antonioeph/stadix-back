from fastapi import APIRouter, HTTPException
from app.schemas import SamplingRequest
from app.services.sampling import calculate_sample_size

router = APIRouter()

@router.post("/calculate")
async def get_sample_size(payload: SamplingRequest):
    # Validaciones básicas
    if not (0 < payload.confidence_level < 1):
        raise HTTPException(400, "El nivel de confianza debe estar entre 0 y 1 (ej: 0.95).")
    if not (0 < payload.margin_error < 1):
        raise HTTPException(400, "El margen de error debe estar entre 0 y 1 (ej: 0.05).")
    if not (0 <= payload.p <= 1):
        raise HTTPException(400, "La proporción 'p' debe estar entre 0 y 1.")

    return calculate_sample_size(
        payload.confidence_level, 
        payload.margin_error, 
        payload.p, 
        payload.population
    )