import numpy as np
from scipy import stats

def calculate_regression(x: list, y: list):
    """
    Calcula Regresión Lineal, Correlación y Covarianza entre dos variables.
    """
    # Validación básica
    if len(x) != len(y):
        return {"error": "Las listas X e Y deben tener el mismo número de datos."}
    
    if len(x) < 2:
        return {"error": "Se necesitan al menos 2 pares de datos."}

    # a arrays de Numpy para eficiencia
    arr_x = np.array(x)
    arr_y = np.array(y)
    
    # 1. Regresión Lineal (Tema 4.2)
    # linregress devuelve: pendiente (m), intercepto (b), r, valor p, error est.
    slope, intercept, r_value, p_value, std_err = stats.linregress(arr_x, arr_y)
    
    # 2. Correlación (Tema 4.3)
    pearson_r = r_value
    r_squared = r_value ** 2 # Coeficiente de determinación
    
    # 3. Covarianza (Tema 4.4)
    # numpy.cov devuelve una matriz de covarianza. [0][1] es la covarianza entre x e y.
    # bias=False usa (n-1) grados de libertad (Muestral), que es lo estándar en inferencia.
    cov_matrix = np.cov(arr_x, arr_y, bias=False)
    covariance = cov_matrix[0][1]
    
    # Interpretación didáctica automática
    strength = "Débil"
    if abs(pearson_r) > 0.4: strength = "Moderada"
    if abs(pearson_r) > 0.7: strength = "Fuerte"
    if abs(pearson_r) > 0.9: strength = "Muy Fuerte"
    
    direction = "Positiva" if pearson_r > 0 else "Negativa"

    return {
        "n": len(x),
        "linear_regression": {
            "slope": float(slope),          # m
            "intercept": float(intercept),  # b
            "equation": f"y = {slope:.4f}x + {intercept:.4f}",
            "r_squared": float(r_squared)
        },
        "correlation": {
            "pearson_r": float(pearson_r),
            "interpretation": f"Correlación {strength} {direction}"
        },
        "covariance": float(covariance)
    }