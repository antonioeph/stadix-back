from fastapi import APIRouter, HTTPException
from app.schemas import BinomialRequest, PoissonRequest, NormalRequest
from app.services.probability import calculate_binomial, calculate_poisson, calculate_normal

router = APIRouter()

@router.post("/binomial")
async def get_binomial(payload: BinomialRequest):
    res = calculate_binomial(payload.n, payload.p, payload.k)
    if "error" in res: raise HTTPException(400, res["error"])
    return res

@router.post("/poisson")
async def get_poisson(payload: PoissonRequest):
    res = calculate_poisson(payload.lam, payload.k)
    if "error" in res: raise HTTPException(400, res["error"])
    return res

@router.post("/normal")
async def get_normal(payload: NormalRequest):
    res = calculate_normal(payload.mean, payload.std, payload.x)
    if "error" in res: raise HTTPException(400, res["error"])
    return res