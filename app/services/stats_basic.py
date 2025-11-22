import pandas as pd
import numpy as np
import math
from scipy import stats

def calculate_descriptive_stats(data: list):
    """
    Genera estadísticas descriptivas y tabla de frecuencias para datos cuantitativos.
    """
    df = pd.DataFrame({'values': data})
    series = df['values']
    n = len(series)
    
    # 1. Estadísticos Básicos (Tendencia Central y Dispersión)
    mean_val = series.mean()
    median_val = series.median()
    
    # Moda (puede haber múltiples)
    mode_result = series.mode()
    mode_val = list(mode_result) if not mode_result.empty else []

    # Dispersión
    variance_val = series.var(ddof=1) # Muestral
    std_dev_val = series.std(ddof=1)  # Muestral
    min_val = series.min()
    max_val = series.max()
    rango = max_val - min_val

    cv_val = (std_dev_val / abs(mean_val)) * 100 if mean_val != 0 else 0.0

    # Q1 = Percentil 25, Q3 = Percentil 75
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1  # Rango Intercuartílico

    # 2. Generación de Tabla de Frecuencias (Datos Agrupados)
    # Regla de Sturges: k = 1 + 3.322 * log10(n)
    k = 1 + 3.322 * math.log10(n)
    k = round(k)
    # Ajuste mínimo de intervalos para evitar errores con pocos datos
    if k < 5: k = 5 
    
    # Amplitud (Width)
    amplitude = rango / k
    
    # Crendolos bins (intervalos)
    # Se extiende un poco el límite superior para incluir el valor máximo
    bins = np.linspace(min_val, max_val + (amplitude*0.01), k+1)
    
    # Pandas cut para agrupar
    df['interval'] = pd.cut(series, bins=bins, right=False, include_lowest=True)
    
    # Agrupación
    freq_table = df.groupby('interval', observed=False).count()
    freq_table = freq_table.rename(columns={'values': 'absolute_freq'})
    
    # Cálculos de columnas adicionales
    freq_table['cumulative_freq'] = freq_table['absolute_freq'].cumsum()
    freq_table['relative_freq'] = freq_table['absolute_freq'] / n
    freq_table['percentage'] = freq_table['relative_freq'] * 100
    freq_table['cumulative_percentage'] = freq_table['percentage'].cumsum()

    # Formateo de salida para JSON
    table_data = []
    for i, (interval, row) in enumerate(freq_table.iterrows()):
        lower = interval.left
        upper = interval.right
        class_mark = (lower + upper) / 2 # Marca de clase (xi)
        
        table_data.append({
            "interval_index": i + 1,
            "lower_limit": round(lower, 2),
            "upper_limit": round(upper, 2),
            "class_mark": round(class_mark, 2),
            "absolute_freq": int(row['absolute_freq']),
            "cumulative_freq": int(row['cumulative_freq']),
            "relative_freq": round(row['relative_freq'], 4),
            "percentage": round(row['percentage'], 2)
        })

    return {
        "summary_stats": {
            "n": int(n),
            "min": float(min_val),
            "max": float(max_val),
            "range": float(rango),
            "mean": float(mean_val),
            "median": float(median_val),
            "mode": [float(m) for m in mode_val],
            "variance": float(variance_val),
            "std_dev": float(std_dev_val),
            "coeff_variation": float(cv_val),
            "q1": float(q1),   
            "q3": float(q3),   
            "iqr": float(iqr)  
        },
        "frequency_table": table_data
    }