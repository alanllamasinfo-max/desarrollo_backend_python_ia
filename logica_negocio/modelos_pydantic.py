from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LlamadaBase(BaseModel):
    nombre_archivo: str
    tamano_kb: float

class LlamadaRespuesta(LlamadaBase):
    id_llamada: str
    estado: str = "pendiente"
    fecha_creacion: datetime

    class Config:
        from_attributes = True