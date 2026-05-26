from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(BASE_DIR / ".env")

# Base
ENVIRONMENT = env("ENVIRONMENT", default="local")
SECRET_KEY = env("SECRET_KEY", default="django-insecure")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
TIME_ZONE = env("TIME_ZONE", default="Asia/Yekaterinburg")

# Toggle apps
SILK_ENABLED = env.bool("SILK_ENABLED", default=True)
AXES_ENABLED = env.bool("AXES_ENABLED", default=True)
ZEAL_ENABLED = env.bool("ZEAL_ENABLED", default=True)
LOGGING_ENABLED = env.bool("LOGGING_ENABLED", default=True)

# Axes
AXES_FAILURE_TRIES = env.int("AXES_FAILURE_TRIES", default=5)
AXES_COOLOFF_MINUTES = env.int("AXES_COOLOFF_MINUTES", default=15)

# Database
DATABASE_ENGINE = env("DATABASE_ENGINE", default="django.db.backends.sqlite3")  # django.db.backends.postgresql
POSTGRES_DB = env("POSTGRES_DB", default="django-template")
POSTGRES_USER = env("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", default="postgres")
POSTGRES_HOST = env("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)

# CORS
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://localhost:8083",
        "http://localhost:8084",
        "http://localhost:8085",
    ],
)
CORS_ALLOW_ALL_ORIGINS = env.bool(
    "CORS_ALLOW_ALL_ORIGINS",
    default=ENVIRONMENT == "local",
)
