import pandas as pd
import numpy as np

def infer_variable_type(data: list):
    """
    Analiza una lista de datos e infiere si es cualitativa, cuantitativa discreta o continua.
    """
    # Convertimos a DataFrame para usar el poder de Pandas
    df = pd.DataFrame({'values': data})
    
    # Limpieza básica: Eliminar nulos si existen
    df = df.dropna()
    
    if df.empty:
        return {
            "type": "error",
            "subtype": "empty",
            "message": "El conjunto de datos está vacío."
        }

    # INTENTO 1: ¿Es numérico?
    try:
        # errors='raise' hará que falle si hay texto que no sea número
        pd.to_numeric(df['values'], errors='raise')
        is_numeric = True
    except ValueError:
        is_numeric = False

    # LÓGICA DE DECISIÓN
    if not is_numeric:
        # --- CAMINO CUALITATIVO ---
        unique_count = df['values'].nunique()
        total_count = len(df)
        
        return {
            "type": "qualitative",
            "subtype": "nominal", # Por defecto asumimos nominal
            "message": f"Detectamos datos de texto. Es una variable Cualitativa.",
            "meta": {
                "unique_values": unique_count,
                "total_samples": total_count
            }
        }
    else:
        # --- CAMINO CUANTITATIVO ---
        # Convertimos la columna a números reales para analizarla
        numeric_series = pd.to_numeric(df['values'])
        
        # Detectar si hay decimales
        # (x % 1 != 0) devuelve True si el número tiene decimales
        has_floats = numeric_series.apply(lambda x: float(x) % 1 != 0).any()
        
        unique_count = numeric_series.nunique()
        
        if has_floats:
            return {
                "type": "quantitative",
                "subtype": "continuous", 
                "message": "Detectamos números con decimales. Es una variable Cuantitativa Continua."
            }
        else:
            # Si son enteros, pero hay "demasiados" valores únicos (ej. > 20), 
            # a veces conviene tratarlos como continuos en estadística, 
            # pero teóricamente son discretos. Aquí seremos puristas por ahora.
            return {
                "type": "quantitative",
                "subtype": "discrete", 
                "message": "Detectamos solo números enteros. Es una variable Cuantitativa Discreta."
            }