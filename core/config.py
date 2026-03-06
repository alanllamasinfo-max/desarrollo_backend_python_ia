import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PPROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI Call Center")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
settings = Settings()