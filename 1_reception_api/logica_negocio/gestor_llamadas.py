import os
import shutil
from acceso_datos.repositorio_llamadas import RepositorioLlamadas
from infraestructura.rabbitmq_cliente import RabbitMQCliente
import uuid

class GestorLlamadas:
    def __init__(self):
        self.repo = RepositorioLlamadas()
        self.rabbit = RabbitMQCliente()
        # Ruta dentro del contenedor (mapeada al volumen compartido)
        self.ruta_almacen = "/app/audios"

    def procesar_llamada(self, archivo_raw, db):
        # 0. Asegurar que la carpeta existe
        if not os.path.exists(self.ruta_almacen):
            os.makedirs(self.ruta_almacen)

        # 1. Generar identidad de la llamada
        id_llamada = str(uuid.uuid4())
        nombre_archivo = f"{id_llamada}_{archivo_raw.filename}"
        ruta_final = os.path.join(self.ruta_almacen, nombre_archivo)

        # 2. GUARDADO FÍSICO (El archivo pasa del navegador al disco)
        with open(ruta_final, "wb") as buffer:
            shutil.copyfileobj(archivo_raw.file, buffer)

        # 3. Guardar en Base de Datos
        # Calculamos el tamaño en KB para el registro
        tamano_kb = os.path.getsize(ruta_final) / 1024
        
        nueva_llamada = self.repo.crear_llamada(
            db, 
            id_llamada=id_llamada, 
            archivo=nombre_archivo, 
            tamano=tamano_kb
        )

        # 4. Notificar al Worker de IA vía RabbitMQ
        mensaje = {
            "id_llamada": id_llamada,
            "archivo": nombre_archivo
        }
        self.rabbit.enviar_mensaje("cola_transcripcion", mensaje)

        return nueva_llamada