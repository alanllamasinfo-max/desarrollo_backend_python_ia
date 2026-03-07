from sqlalchemy import Column, String, Float, DateTime, Text
from infraestructura.db_conexion import Base
import datetime

class LlamadaSQL(Base):
    __tablename__ = "llamadas"

    id_llamada = Column(String, primary_key=True, index=True)
    nombre_archivo = Column(String)
    tamano_kb = Column(Float)
    estado = Column(String, default="recibido")
    transcripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)