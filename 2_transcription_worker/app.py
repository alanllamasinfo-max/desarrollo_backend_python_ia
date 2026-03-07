import pika
import json
import os
import time
from procesador_ia import TranscriptorIA
from db_actualizador import DBActualizador

# Esperar a que RabbitMQ esté listo (reintento simple)
time.sleep(10) 

def procesar_mensaje(ch, method, properties, body):
    datos = json.loads(body)
    id_llamada = datos['id_llamada']
    nombre_archivo = datos['archivo']
    
    # 1. Ruta del archivo en el volumen compartido
    ruta_audio = f"/app/audios/{nombre_archivo}"
    
    try:
        # 2. IA trabajando
        ia = TranscriptorIA()
        texto = ia.transcribir(ruta_audio)
        
        # 3. Guardar en Postgres
        db = DBActualizador()
        db.guardar_transcripcion(id_llamada, texto)
        
        print(f" [OK] Llamada {id_llamada} procesada con éxito.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f" [ERROR] Fallo al procesar {id_llamada}: {e}")
        # En producción aquí decidirías si reintentar o mandar a una cola de errores

# Configuración de RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='cola_transcripcion')

channel.basic_consume(queue='cola_transcripcion', on_message_callback=procesar_mensaje)

print(' [*] Worker de IA esperando audios...')
channel.start_consuming()