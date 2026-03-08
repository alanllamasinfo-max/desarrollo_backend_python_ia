import os
import shutil
import uuid
from acceso_datos.repositorio_llamadas import RepositorioLlamadas
from infraestructura.rabbitmq_cliente import RabbitMQCliente

class GestorLlamadas:
    def __init__(self, db_session):
        self.repo = RepositorioLlamadas(db_session)
        self.rabbit = RabbitMQCliente()
        self.db = db_session
        self.ruta_almacen = "/app/audios"
        
    async def procesar_llamada(self, archivo_raw):
        if not os.path.exists(self.ruta_almacen):
            os.makedirs(self.ruta_almacen)
        
        id_llamada = str(uuid.uuid4())
        nombre_archivo = f"{id_llamada}_{archivo_raw.filename}"
        ruta_final = os.path.join(self.ruta_almacen, nombre_archivo)
        
        with open(ruta_final, "wb") as buffer:
            shutil.copyfileobj(archivo_raw.file, buffer)
        
        tamano_kb = os.path.getsize(ruta_final) / 1024
        
        datos = {
            "id_llamada": id_llamada,
            "nombre_archivo": nombre_archivo,
            "tamano_kb": tamano_kb,
            "estado": "recibido"
        }
        
        nueva_llamada = self.repo.guardar_llamada(datos)
        
        mensaje = {
            "id_llamada": id_llamada,
            "archivo": nombre_archivo
        }
        self.rabbit.enviar_mensaje(mensaje)
        
        return nueva_llamada