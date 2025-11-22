from fastapi import APIRouter, HTTPException,UploadFile, File
from app.schemas import RegressionRequest, InferenceResponse
from app.services.inference import calculate_regression
import pandas as pd
import io

router = APIRouter()

@router.post("/regression", response_model=InferenceResponse)
async def get_regression_analysis(payload: RegressionRequest):
    result = calculate_regression(payload.x_data, payload.y_data)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.post("/upload", response_model=InferenceResponse)
async def upload_bivariate_dataset(file: UploadFile = File(...)):
    """
    Lee un archivo (Excel/CSV) y usa las dos primeras columnas numéricas como X e Y.
    """
    try:
        contents = await file.read()
        
        # 1. Leer archivo (sin encabezados para evitar perder datos)
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), header=None)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents), header=None)
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Usa .csv o .xlsx")

        # 2. Limpieza y Selección de Columnas
        # Intentamos convertir todo a números, lo que no sea número se vuelve NaN
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Eliminamos filas que tengan NaN en CUALQUIERA de las columnas (para mantener pares X,Y)
        df = df.dropna()

        # Verificamos tener al menos 2 columnas y 2 filas
        if df.shape[1] < 2:
            raise HTTPException(status_code=400, detail="El archivo debe tener al menos 2 columnas (X e Y).")
        if df.shape[0] < 2:
            raise HTTPException(status_code=400, detail="Se necesitan al menos 2 filas de datos.")

        # 3. Asignación: Col 0 -> X, Col 1 -> Y
        x_data = df.iloc[:, 0].tolist()
        y_data = df.iloc[:, 1].tolist()

        result = calculate_regression(x_data, y_data)

        if "error" not in result:
            # campos extra al diccionario de respuesta
            # Aunque no estén en el Schema estricto, FastAPI los dejará pasar si es dict
            return {**result, "raw_x": x_data, "raw_y": y_data}

        # 4. Cálculo
        return result

    except Exception as e:
        print(f"Error procesando archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")