from fastapi import APIRouter, HTTPException,UploadFile, File
from app.schemas import AnalysisRequest, DescriptiveResponse
from app.services.stats_basic import calculate_descriptive_stats
import pandas as pd
import io

router = APIRouter()

@router.post("/basic", response_model=DescriptiveResponse)
async def get_descriptive_stats(payload: AnalysisRequest):
    # Validar que haya datos
    if not payload.sample_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos.")
        
    try:
        # Se convierte todo a float para asegurar matemáticas correctas
        clean_data = [float(x) for x in payload.sample_data]
        
        result = calculate_descriptive_stats(clean_data)
        return result
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Para estadística descriptiva, todos los datos deben ser numéricos.")
    except Exception as e:
        print(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar los cálculos estadísticos.")
    
@router.post("/upload", response_model=DescriptiveResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """
    Recibe un archivo Excel (.xlsx) o CSV, toma la PRIMERA columna numérica
    y calcula las estadísticas descriptivas.
    """
    try:
        contents = await file.read()
        
        # 1. Detectar formato y crear DataFrame
        if file.filename.endswith('.csv'):
            # Leemos CSV
            df = pd.read_csv(io.BytesIO(contents),header=None)
        elif file.filename.endswith(('.xls', '.xlsx')):
            # Leemos Excel (requiere openpyxl instalado en el backend)
            df = pd.read_excel(io.BytesIO(contents),header=None)
        else:
            raise HTTPException(status_code=400, detail="Formato no válido. Usa .csv o .xlsx")

        # 2. Limpieza: Aplanar datos
        # Tomamos la primera columna que encuentre (asumimos formato simple)
        first_column_data = df.iloc[:, 0].tolist()
        
        # 3. Validar que sean números
        # Filtramos solo lo que se pueda convertir a float
        clean_data = []
        for x in first_column_data:
            try:
                val = float(x)
                # Ignorar NaN (Not a Number) de pandas
                if not pd.isna(val):
                    clean_data.append(val)
            except:
                continue # Si es texto, lo saltamos

        if len(clean_data) == 0:
            raise HTTPException(status_code=400, detail="El archivo no contiene datos numéricos válidos en la primera columna.")

        # 4. Reutilizamos la lógica de cálculo existente
        return calculate_descriptive_stats(clean_data)

    except Exception as e:
        print(f"Error procesando archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")