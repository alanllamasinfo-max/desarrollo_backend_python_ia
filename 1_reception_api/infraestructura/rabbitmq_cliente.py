import pika
import json

class RabbitMQCliente:
    def __init__(self):
        # En Docker, el host será el nombre del servicio 'rabbitmq'
        self.host = "rabbitmq"
        self.queue = "cola_transcripcion"

    def enviar_mensaje(self, cuerpo_mensaje: dict):
        # 1. Establecer conexión
        conexion = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        canal = conexion.channel()

        # 2. Asegurarse de que la cola exista
        canal.queue_declare(queue=self.queue)

        # 3. Publicar el mensaje
        canal.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=json.dumps(cuerpo_mensaje)
        )
        
        print(f" [x] Mensaje enviado a RabbitMQ: {cuerpo_mensaje}")
        conexion.close()