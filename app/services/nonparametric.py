import numpy as np
from scipy import stats

def calculate_chi_square(matrix: list):
    """
    Calcula la prueba de independencia Chi-Cuadrada dada una tabla de contingencia (matriz).
    """
    # Validar que sea una matriz válida (mismas columnas en cada fila)
    if not matrix or not matrix[0]:
        return {"error": "La matriz de datos está vacía."}
    
    row_len = len(matrix[0])
    for row in matrix:
        if len(row) != row_len:
            return {"error": "Todas las filas deben tener el mismo número de columnas."}

    # Cálculo con Scipy
    # devuelve: chi2_stat, p_value, dof, expected_matrix
    chi2, p, dof, expected = stats.chi2_contingency(matrix)

    # Interpretación automática (con alfa = 0.05 estándar)
    significant = p < 0.05
    interpretation = "Existe dependencia significativa entre las variables (Rechazamos H0)." if significant else "No existe evidencia de relación (No rechazamos H0)."

    return {
        "statistic": float(chi2),
        "p_value": float(p),
        "dof": int(dof),
        "expected_frequencies": expected.tolist(),
        "interpretation": interpretation,
        "is_significant": significant
    }