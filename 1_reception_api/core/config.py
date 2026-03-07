import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Call Center - Reception"
    # Por ahora usamos una URL por defecto para Docker
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/callcenter_db")

settings = Settings()