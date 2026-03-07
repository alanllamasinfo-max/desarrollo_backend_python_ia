import whisper

class TranscriptorIA:
    def __init__(self):
        # Cargamos el modelo "base" (balance entre velocidad y precisión)
        self.model = whisper.load_model("base")

    def transcribir(self, ruta_archivo: str):
        print(f"--- Iniciando transcripción de: {ruta_archivo} ---")
        # Aquí la IA hace la magia
        result = self.model.transcribe(ruta_archivo)
        return result["text"]
