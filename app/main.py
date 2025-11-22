from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import variables,descriptive,inference,nonparametric,probability,hypothesis,sampling


app = FastAPI(title="Estadística Didáctica API")

# Configuración CORS (para que Next.js hable con Python)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de prueba
@app.get("/")
def read_root():
    return {"message": "API de Estadística Operativa"}

# --- REGISTRO DE ROUTERS ---
# prefijo /api/v1/variables para que la ruta final sea clara
app.include_router(variables.router, prefix="/api/v1/variables", tags=["Variables"])
app.include_router(descriptive.router, prefix="/api/v1/descriptive", tags=["Descriptive"])
app.include_router(inference.router, prefix="/api/v1/inference", tags=["Inference"])
app.include_router(nonparametric.router, prefix="/api/v1/nonparametric", tags=["NonParametric"])
app.include_router(probability.router, prefix="/api/v1/probability", tags=["Probability"]) 
app.include_router(hypothesis.router, prefix="/api/v1/hypothesis", tags=["Hypothesis"]) # Pruebas T / ANOVA
app.include_router(sampling.router, prefix="/api/v1/sampling", tags=["Sampling"]) 
