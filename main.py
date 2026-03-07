from fastapi import FastAPI
from presentacion.rutas_audio import router as rutas_audio
from infraestructura.db_conexion import engine, Base
from acceso_datos import modelos_sql

# Creamos las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Recepción de Llamadas - AI Call Center")

# Conectamos la Capa de Presentación (El Camarero)
app.include_router(rutas_audio)

@app.get("/")
def inicio():
    return {"mensaje": "Servidor de Recepción de IA funcionando correctamente"}