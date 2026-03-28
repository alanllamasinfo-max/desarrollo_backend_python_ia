# 📞 VoiceFlow API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Sistema de gestión de llamadas de audio en tiempo real con arquitectura orientada a eventos.**

[Ver Demo](#demo) · [Documentación API](#api) · [Instalación rápida](#instalación)

</div>

---

## 📌 Descripción

**VoiceFlow API** es un microservicio backend que gestiona el ciclo de vida completo de llamadas de audio: recepción, encolado asíncrono, procesamiento y persistencia. Diseñado con una arquitectura limpia por capas y comunicación basada en eventos mediante RabbitMQ.

> Ideal como base para sistemas de call center, grabación de llamadas, o pipelines de procesamiento de audio.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente HTTP                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST / Multipart Audio
┌──────────────────────────▼──────────────────────────────────┐
│               Capa de Presentación (FastAPI)                 │
│                   presentacion/rutas_audio.py                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Capa de Lógica de Negocio                       │
│         logica_negocio/gestor_llamadas.py                    │
│         logica_negocio/modelos_pydantic.py                   │
└────────────────┬─────────────────────┬──────────────────────┘
                 │                     │
┌────────────────▼──────┐   ┌──────────▼──────────────────────┐
│  Acceso a Datos       │   │  Infraestructura                 │
│  (SQLAlchemy)         │   │  (RabbitMQ Cliente)              │
│  acceso_datos/        │   │  infraestructura/                │
└────────────────┬──────┘   └──────────┬──────────────────────┘
                 │                     │
┌────────────────▼──────┐   ┌──────────▼──────────────────────┐
│      PostgreSQL       │   │         RabbitMQ Broker          │
│      (Persistencia)   │   │      (Cola de eventos)           │
└───────────────────────┘   └─────────────────────────────────┘
```

---

## ✨ Características principales

| Feature | Descripción |
|---|---|
| 🎙️ **Ingesta de audio** | Recepción de archivos de audio vía API REST (multipart/form-data) |
| ⚡ **Procesamiento asíncrono** | Publicación en colas RabbitMQ para desacoplar el procesamiento |
| 🗃️ **Persistencia** | Registro completo del ciclo de vida de cada llamada en PostgreSQL |
| 🧱 **Arquitectura limpia** | Separación estricta en capas: presentación, negocio, datos, infraestructura |
| 📄 **API autodocumentada** | Swagger UI + ReDoc disponibles en `/docs` y `/redoc` |
| 🐳 **Containerizado** | Docker Compose listo para desarrollo y producción |

---

## 🗂️ Estructura del proyecto

```
voiceflow-api/
├── main.py                          # Punto de entrada, configuración FastAPI
├── core/
│   └── config.py                    # Variables de entorno y configuración global
├── presentacion/
│   └── rutas_audio.py               # Endpoints REST (routers FastAPI)
├── logica_negocio/
│   ├── gestor_llamadas.py           # Casos de uso y orquestación
│   └── modelos_pydantic.py          # Esquemas de validación (request/response)
├── acceso_datos/
│   ├── modelos_sql.py               # Modelos ORM (SQLAlchemy)
│   └── repositorio_llamadas.py      # Patrón repositorio - queries a la BD
├── infraestructura/
│   ├── db_conexion.py               # Sesión y engine de base de datos
│   └── rabbitmq_cliente.py          # Cliente de publicación a RabbitMQ
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

---

## 🚀 Instalación

### Prerrequisitos

- Docker 24+ y Docker Compose v2
- Python 3.11+ (solo para desarrollo local sin Docker)

### Con Docker (recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/voiceflow-api.git
cd voiceflow-api

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar todos los servicios
docker compose up -d

# 4. Verificar que todo está en marcha
docker compose ps
```

Los servicios estarán disponibles en:

| Servicio | URL |
|---|---|
| API REST | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| RabbitMQ Management | `http://localhost:15672` |

### Desarrollo local

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Levantar solo las dependencias (BD + RabbitMQ)
docker compose up -d postgres rabbitmq

# Iniciar la API en modo desarrollo (hot-reload)
uvicorn main:app --reload --port 8000
```

---

## 📡 API Reference

La documentación interactiva completa está disponible en **`/docs`** (Swagger UI).

### Endpoints principales

#### `POST /audio/llamadas`
Registra una nueva llamada y la encola para procesamiento.

```bash
curl -X POST http://localhost:8000/audio/llamadas \
  -F "audio=@grabacion.wav" \
  -F "duracion_segundos=120" \
  -F "telefono_origen=+34600000000"
```

**Response `201 Created`:**
```json
{
  "id": "a1b2c3d4-...",
  "estado": "encolada",
  "mensaje": "Llamada registrada y encolada para procesamiento"
}
```

#### `GET /audio/llamadas/{id}`
Consulta el estado de una llamada por su ID.

#### `GET /audio/llamadas`
Lista todas las llamadas con paginación.

---

## ⚙️ Variables de entorno

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/voiceflow_db

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_QUEUE=llamadas_queue

# Aplicación
APP_ENV=development
LOG_LEVEL=INFO
```

---

## 🧪 Tests

```bash
# Ejecutar tests unitarios
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html
```

---

## 🛠️ Stack tecnológico

- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web asíncrono de alto rendimiento
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM con soporte async
- **[Pika / aio-pika](https://aio-pika.readthedocs.io/)** — Cliente RabbitMQ para Python
- **[Pydantic v2](https://docs.pydantic.dev/)** — Validación y serialización de datos
- **[PostgreSQL](https://www.postgresql.org/)** — Base de datos relacional
- **[RabbitMQ](https://www.rabbitmq.com/)** — Message broker
- **[Docker Compose](https://docs.docker.com/compose/)** — Orquestación de contenedores

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

---

<div align="center">

Hecho con ☕ y Python · [⬆ Volver arriba](#-voiceflow-api)

</div>
