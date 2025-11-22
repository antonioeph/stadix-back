import math
from scipy import stats

def calculate_sample_size(confidence_level: float, margin_error: float, p: float = 0.5, population: int = None):
    """
    Calcula el tamaño de la muestra.
    confidence_level: 0.90, 0.95, 0.99 (decimal)
    margin_error: 0.05 (decimal)
    p: Proporción esperada (default 0.5 para máxima varianza)
    population: Tamaño de población (N). Si es None o 0, se asume infinita.
    """
    
    # 1. Obtener Z Score desde la confianza
    # alpha = 1 - confianza
    # Z = stats.norm.ppf(1 - alpha/2)
    alpha = 1 - confidence_level
    z_score = stats.norm.ppf(1 - alpha/2)
    
    q = 1 - p
    e_squared = margin_error ** 2
    z_squared = z_score ** 2
    
    # Numerador común (Z^2 * p * q)
    numerator = z_squared * p * q
    
    if population and population > 0:
        # --- POBLACIÓN FINITA ---
        # n = (N * Z^2 * p * q) / (e^2 * (N-1) + Z^2 * p * q)
        num_finite = population * numerator
        den_finite = (e_squared * (population - 1)) + numerator
        n = num_finite / den_finite
        formula_used = "Finita (Conoce N)"
    else:
        # --- POBLACIÓN INFINITA ---
        # n = (Z^2 * p * q) / e^2
        n = numerator / e_squared
        formula_used = "Infinita (Desconoce N)"
    
    # Redondear siempre hacia arriba para asegurar la muestra
    n_rounded = math.ceil(n)
    
    return {
        "sample_size": int(n_rounded),
        "z_score": float(z_score),
        "p_value": float(p),
        "q_value": float(q),
        "formula": formula_used,
        "is_finite": population is not None and population > 0
    }