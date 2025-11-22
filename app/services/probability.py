from scipy import stats
import numpy as np

def calculate_binomial(n: int, p: float, k: int):
    """
    Probabilidad de obtener exactamente k éxitos en n ensayos.
    """
    if not (0 <= p <= 1):
        return {"error": "La probabilidad 'p' debe estar entre 0 y 1."}
    if k > n:
        return {"error": "k (éxitos) no puede ser mayor que n (ensayos)."}

    prob_exact = stats.binom.pmf(k, n, p)  # P(X=k)
    prob_acum = stats.binom.cdf(k, n, p)   # P(X<=k)
    mean = n * p
    variance = n * p * (1 - p)

    return {
        "distribution": "Binomial",
        "prob_exact": float(prob_exact),
        "prob_accumulated": float(prob_acum),
        "expected_value": float(mean),
        "variance": float(variance)
    }

def calculate_poisson(lam: float, k: int):
    """
    Probabilidad de que ocurran k eventos dada una tasa media lambda.
    """
    if lam <= 0:
        return {"error": "Lambda debe ser mayor a 0."}

    prob_exact = stats.poisson.pmf(k, lam)
    prob_acum = stats.poisson.cdf(k, lam)

    return {
        "distribution": "Poisson",
        "prob_exact": float(prob_exact),
        "prob_accumulated": float(prob_acum),
        "expected_value": float(lam)
    }

def calculate_normal(mean: float, std: float, x: float):
    """
    Calcula Z y el área bajo la curva (probabilidad) hasta x.
    """
    if std <= 0:
        return {"error": "La desviación estándar debe ser positiva."}

    # Estandarización Z
    z_score = (x - mean) / std
    
    # Área a la izquierda (Cumulative Density Function)
    area_left = stats.norm.cdf(x, mean, std)
    area_right = 1 - area_left

    return {
        "distribution": "Normal",
        "z_score": float(z_score),
        "prob_left": float(area_left),  # P(X < x)
        "prob_right": float(area_right) # P(X > x)
    }