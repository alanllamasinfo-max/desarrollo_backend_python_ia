from fastapi import FastAPI
from presentacion.rutas_audio import router as rutas_audio

app = FastAPI(title="API de Recepción de Llamadas - AI Call Center")

# Conectamos la Capa de Presentación (El Camarero)
app.include_router(rutas_audio)

@app.get("/")
def inicio():
    return {"mensaje": "Servidor de Recepción de IA funcionando correctamente"}