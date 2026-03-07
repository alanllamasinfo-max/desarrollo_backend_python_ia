from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import time

class DBActualizador:
    def __init__(self):
        # Leemos la URL desde el entorno que configuramos en docker-compose
        self.db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/callcenter_db")
        self.engine = create_engine(
            self.db_url,
            pool_pre_ping=True, # Verifica que la conexión esté viva antes de usarla
            pool_recycle=3600    # Reinicia conexiones viejas
        )

    def guardar_transcripcion(self, id_llamada: str, texto: str, intentos=3):
        query = text("""
            UPDATE llamadas 
            SET transcripcion = :texto, estado = 'completado' 
            WHERE id_llamada = :id
        """)
        
        for intento in range(intentos):
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(query, {"texto": texto, "id": id_llamada})
                    conn.commit()
                    
                    if result.rowcount == 0:
                        print(f" [!] Advertencia: No se encontró la llamada {id_llamada} para actualizar.")
                    else:
                        print(f" [db] Transcripción guardada con éxito para {id_llamada}")
                    return True # Éxito
            
            except SQLAlchemyError as e:
                print(f" [!] Error de DB (intento {intento + 1}/{intentos}): {e}")
                time.sleep(2) # Esperar un poco antes de reintentar
                
        print(f" [ERROR] No se pudo actualizar la DB tras {intentos} intentos.")
        return False