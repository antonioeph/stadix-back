from fastapi import APIRouter, HTTPException
from app.schemas import TOneSampleRequest, TIndependentRequest, AnovaRequest
from app.services.hypothesis import calculate_t_test_one_sample, calculate_t_test_independent, calculate_anova

router = APIRouter()

@router.post("/t-test-one")
async def t_test_one(payload: TOneSampleRequest):
    res = calculate_t_test_one_sample(payload.data, payload.mu)
    if "error" in res: raise HTTPException(400, res["error"])
    return res

@router.post("/t-test-ind")
async def t_test_ind(payload: TIndependentRequest):
    res = calculate_t_test_independent(payload.group1, payload.group2)
    if "error" in res: raise HTTPException(400, res["error"])
    return res

@router.post("/anova")
async def anova_test(payload: AnovaRequest):
    res = calculate_anova(payload.groups)
    if "error" in res: raise HTTPException(400, res["error"])
    return res