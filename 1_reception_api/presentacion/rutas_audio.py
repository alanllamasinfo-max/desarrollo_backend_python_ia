from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from infraestructura.db_conexion import get_db
from logica_negocio.gestor_llamadas import GestorLlamadas
import shutil
import os

router = APIRouter()

# Definimos la ruta donde se guardarán los audios dentro del contenedor
UPLOAD_DIR = "/app/audios"

@router.post("/subir-audio")
async def recibir_audio(archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Creamos el directorio si no existe (por si acaso)
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    ruta_final = os.path.join(UPLOAD_DIR, archivo.filename)

    try:
        gestor = GestorLlamadas(db)
        resultado = await gestor.procesar_llamada(archivo)
        
        return {
            "mensaje": "Audio recibido y en cola de transcripción",
            "llamada": resultado
        }

    except Exception as e:
        # Si algo falla, lanzamos un error 500 para ver el detalle en los logs
        raise HTTPException(status_code=500, detail=f"Error al procesar audio: {str(e)}")