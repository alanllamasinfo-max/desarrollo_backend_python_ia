from sqlalchemy.orm import Session
from .modelos_sql import LlamadaSQL

class RepositorioLlamadas:
    def __init__(self, db: Session):
        self.db = db

    def guardar_llamada(self, datos_llamada: dict):
        nueva_llamada = LlamadaSQL(
            id_llamada=datos_llamada["id_llamada"],
            nombre_archivo=datos_llamada["nombre_archivo"],
            tamano_kb=datos_llamada["tamano_kb"],
            estado=datos_llamada["estado"]
        )
        self.db.add(nueva_llamada)
        self.db.commit()
        self.db.refresh(nueva_llamada)
        return nueva_llamada