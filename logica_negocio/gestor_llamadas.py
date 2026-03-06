import uuid
from fastapi import HTTPException
from acceso_datos.repositorio_llamadas import RepositorioLlamadas
from infraestructura.rabbitmq_cliente import RabbitMQCliente

class GestorLlamadas:
    def __init__(self, db_session):
        self.repo = RepositorioLlamadas(db_session)
        self.rabbit = RabbitMQCliente() # Capa 4: Adaptador

    async def procesar_nueva_llamada(self, nombre_archivo: str, tamano_bytes: int):
        # 1. Regla de Negocio
        if tamano_bytes / (1024 * 1024) > 10:
            raise HTTPException(status_code=400, detail="Archivo demasiado grande")

        datos_iniciales = {
            "id_llamada": str(uuid.uuid4()),
            "nombre_archivo": nombre_archivo,
            "tamano_kb": tamano_bytes / 1024,
            "estado": "recibido"
        }

        # 2. Capa 3: Guardar en Postgres
        llamada_guardada = self.repo.guardar_llamada(datos_iniciales)
        
        # 3. Capa 4: Notificar a RabbitMQ para que la IA empiece a trabajar
        mensaje_para_ia = {
            "id_llamada": llamada_guardada.id_llamada,
            "archivo": llamada_guardada.nombre_archivo
        }
        self.rabbit.enviar_mensaje(mensaje_para_ia)
        
        return llamada_guardada