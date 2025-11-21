from pydantic import BaseModel
from typing import List, Any, Optional

# Lo que el usuario nos envía
class AnalysisRequest(BaseModel):
    sample_data: List[Any] # Puede ser una lista de lo que sea (números o texto)

# La respuesta educativa que devolvemos
class EducationalContext(BaseModel):
    explanation: str
    suggested_charts: List[str]

# La respuesta completa del servidor
class AnalysisResponse(BaseModel):
    variable_type: str     # quantitative / qualitative
    variable_subtype: str  # discrete / continuous / nominal
    message: str
    educational_info: EducationalContext