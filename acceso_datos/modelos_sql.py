from sqlalchemy import Column, String, Float, DateTime
from .db_conexion import Base
import datetime

class LlamadaSQL(Base):
    __tablename__ = "llamadas"

    id_llamada = Column(String, primary_key=True, index=True)
    nombre_archivo = Column(String)
    tamano_kb = Column(Float)
    estado = Column(String, default="recibido")
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)