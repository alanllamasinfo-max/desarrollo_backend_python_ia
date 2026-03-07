from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from infraestructura.db_conexion import get_db
from logica_negocio.gestor_llamadas import GestorLlamadas

router = APIRouter()

@router.post("/subir-audio")
async def recibir_audio(archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    # Pasamos la sesión de DB al gestor
    gestor = GestorLlamadas(db)
    
    resultado = await gestor.procesar_nueva_llamada(
        nombre_archivo=archivo.filename,
        tamano_bytes=archivo.size
    )
    
    return resultado