from fastapi import APIRouter, HTTPException
from app.schemas import AnalysisRequest, AnalysisResponse, EducationalContext
from app.services.data_analysis import infer_variable_type

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_variables(payload: AnalysisRequest):
    
    # 1. Llamamos a la lógica matemática (Service)
    result = infer_variable_type(payload.sample_data)
    
    if result["type"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])


    educ_context = EducationalContext(explanation="", suggested_charts=[])
    
    if result["type"] == "quantitative":
        if result["subtype"] == "discrete":
            educ_context.explanation = "Las variables discretas toman valores contables (ej. número de hijos)."
            educ_context.suggested_charts = ["Diagrama de Barras", "Gráfico de Bastones"]
        else:
            educ_context.explanation = "Las variables continuas pueden tomar infinitos valores en un intervalo (ej. altura, peso)."
            educ_context.suggested_charts = ["Histograma", "Polígono de Frecuencias"]
            
    elif result["type"] == "qualitative":
        educ_context.explanation = "Las variables cualitativas representan categorías o etiquetas sin valor numérico directo."
        educ_context.suggested_charts = ["Gráfico Circular (Pastel)", "Barras Simples"]

    # 3. Devolvemos todo empaquetado
    return AnalysisResponse(
        variable_type=result["type"],
        variable_subtype=result["subtype"],
        message=result["message"],
        educational_info=educ_context
    )