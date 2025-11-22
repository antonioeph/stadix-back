from pydantic import BaseModel
from typing import List, Any, Optional

# Lo que el usuario envía
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

class FrequencyRow(BaseModel):
    interval_index: int
    lower_limit: float
    upper_limit: float
    class_mark: float
    absolute_freq: int
    cumulative_freq: int
    relative_freq: float
    percentage: float

class SummaryStats(BaseModel):
    n: int
    min: float
    max: float
    range: float
    mean: float
    median: float
    mode: List[float]
    variance: float
    std_dev: float
    coeff_variation: float
    q1: float   
    q3: float   
    iqr: float  

class DescriptiveResponse(BaseModel):
    summary_stats: SummaryStats
    frequency_table: List[FrequencyRow]    

# --- MÓDULO 4: INFERENCIA ---

class RegressionRequest(BaseModel):
    x_data: List[float]
    y_data: List[float]

class RegressionResult(BaseModel):
    slope: float
    intercept: float
    equation: str
    r_squared: float

class CorrelationResult(BaseModel):
    pearson_r: float
    interpretation: str

class InferenceResponse(BaseModel):
    n: int
    linear_regression: RegressionResult
    correlation: CorrelationResult
    covariance: float
    raw_x: Optional[List[float]] = None 
    raw_y: Optional[List[float]] = None

# --- MÓDULO 5: NO PARAMÉTRICA ---
class ChiSquareRequest(BaseModel):
    observed_data: List[List[int]] # Matriz de conteos observados

class ChiSquareResponse(BaseModel):
    statistic: float
    p_value: float
    dof: int
    expected_frequencies: List[List[float]]
    interpretation: str
    is_significant: bool

# --- MÓDULO PROBABILIDAD ---
class BinomialRequest(BaseModel):
    n: int
    p: float
    k: int

class PoissonRequest(BaseModel):
    lam: float
    k: int

class NormalRequest(BaseModel):
    mean: float
    std: float
    x: float

class TOneSampleRequest(BaseModel):
    data: List[float]
    mu: float  # Media teórica a comparar

class TIndependentRequest(BaseModel):
    group1: List[float]
    group2: List[float]

class AnovaRequest(BaseModel):
    groups: List[List[float]]  # Matriz de grupos: [[datos_g1], [datos_g2], [datos_g3]]

# --- MÓDULO 6: MUESTREO ---
class SamplingRequest(BaseModel):
    confidence_level: float # Ej: 0.95
    margin_error: float     # Ej: 0.05
    p: float = 0.5          # Ej: 0.5 (Probabilidad de éxito)
    population: Optional[int] = None # Opcional (Tamaño de la población N)