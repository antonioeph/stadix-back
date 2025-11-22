import numpy as np
from scipy import stats

def calculate_t_test_one_sample(data: list, mu: float):
    """
    Prueba T para una muestra. Compara la media de una muestra contra un valor teórico (mu).
    """
    if len(data) < 2:
        return {"error": "Se necesitan al menos 2 datos."}
    
    t_stat, p_value = stats.ttest_1samp(data, mu)
    mean = np.mean(data)
    
    return {
        "test_type": "T-Student (1 muestra)",
        "statistic": float(t_stat),
        "p_value": float(p_value),
        "sample_mean": float(mean),
        "theoretical_mean": float(mu),
        "interpretation": "Rechazamos H0 (Medias diferentes)" if p_value < 0.05 else "No rechazamos H0 (Medias iguales)"
    }

def calculate_t_test_independent(group1: list, group2: list):
    """
    Prueba T para dos muestras independientes. Compara si las medias de dos grupos son diferentes.
    """
    if len(group1) < 2 or len(group2) < 2:
        return {"error": "Cada grupo debe tener al menos 2 datos."}

    t_stat, p_value = stats.ttest_ind(group1, group2)
    
    return {
        "test_type": "T-Student (2 muestras independientes)",
        "statistic": float(t_stat),
        "p_value": float(p_value),
        "mean_group1": float(np.mean(group1)),
        "mean_group2": float(np.mean(group2)),
        "interpretation": "Rechazamos H0 (Existe diferencia significativa)" if p_value < 0.05 else "No rechazamos H0 (No hay diferencia significativa)"
    }

def calculate_anova(groups: list):
    """
    ANOVA de una vía. Compara medias de 3 o más grupos.
    groups: Lista de listas [[g1_data], [g2_data], [g3_data]]
    """
    if len(groups) < 3:
        return {"error": "ANOVA requiere al menos 3 grupos. Para 2 grupos usa T-Student."}
    
    # f_oneway desempaqueta la lista de grupos
    f_stat, p_value = stats.f_oneway(*groups)
    
    means = [float(np.mean(g)) for g in groups]
    
    return {
        "test_type": "ANOVA de una vía",
        "statistic": float(f_stat),
        "p_value": float(p_value),
        "group_means": means,
        "interpretation": "Rechazamos H0 (Al menos un grupo es diferente)" if p_value < 0.05 else "No rechazamos H0 (Medias iguales)"
    }