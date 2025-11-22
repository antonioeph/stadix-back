from fastapi import APIRouter, HTTPException
from app.schemas import ChiSquareRequest, ChiSquareResponse
from app.services.nonparametric import calculate_chi_square

router = APIRouter()

@router.post("/chi-square", response_model=ChiSquareResponse)
async def perform_chi_square(payload: ChiSquareRequest):
    result = calculate_chi_square(payload.observed_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result