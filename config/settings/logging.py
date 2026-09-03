import logging
from typing import TYPE_CHECKING

from config.settings.env import BASE_DIR, LOGGING_ENABLED

if TYPE_CHECKING:
    from pathlib import Path

DEFAULT_LOG_LEVEL = "INFO"
DATABASE_LOG_LEVEL = "WARNING"
REQUEST_LOG_LEVEL = "ERROR"


def build_file_handler(filename: Path, level: str = DEFAULT_LOG_LEVEL) -> dict[str, object]:
    """Создаёт файловый handler с ежедневной ротацией."""
    return {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": level,
        "formatter": "verbose",
        "filename": filename,
        "when": "midnight",
        "interval": 1,
        "backupCount": 7,
        "encoding": "utf-8",
        "utc": False,
        "delay": True,
    }


def build_logger(
    handlers: list[str] | None = None,
    level: str = DEFAULT_LOG_LEVEL,
    *,
    propagate: bool = False,
) -> dict[str, object]:
    """Создаёт конфиг logger."""
    return {
        "handlers": ["console"] if handlers is None else handlers,
        "level": level,
        "propagate": propagate,
    }


def create_log_dir(name: str) -> Path:
    """Создаёт директорию для логов и возвращает путь до неё."""
    log_dir = BASE_DIR / "logs" / name
    log_dir.mkdir(exist_ok=True, parents=True)
    return log_dir


if LOGGING_ENABLED:
    logging.captureWarnings(capture=True)

    DJANGO_LOG_DIR = create_log_dir("django")
    THIRD_PARTY_LOG_DIR = create_log_dir("third_party")
    ROOT_LOG_DIR = create_log_dir("root")

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{asctime}] {levelname:<8} {name}:{lineno} | {message}",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "{levelname:<8} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": DEFAULT_LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "console_warnings": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "root_file": build_file_handler(ROOT_LOG_DIR / "root.log"),
            "django_file": build_file_handler(DJANGO_LOG_DIR / "django.log"),
            "django_request_file": build_file_handler(
                DJANGO_LOG_DIR / "django_request.log",
                level=REQUEST_LOG_LEVEL,
            ),
            "django_db_file": build_file_handler(
                DJANGO_LOG_DIR / "django_db.log",
                level=DATABASE_LOG_LEVEL,
            ),
            "django_server_file": build_file_handler(DJANGO_LOG_DIR / "django_server.log"),
            "django_templates_file": build_file_handler(DJANGO_LOG_DIR / "django_template.log"),
            "django_safe_migrations_file": build_file_handler(THIRD_PARTY_LOG_DIR / "django_safe_migrations.log"),
            "rest_framework_file": build_file_handler(THIRD_PARTY_LOG_DIR / "rest_framework.log"),
            "axes_file": build_file_handler(THIRD_PARTY_LOG_DIR / "axes.log"),
            "silk_file": build_file_handler(THIRD_PARTY_LOG_DIR / "silk.log"),
            "zeal_file": build_file_handler(THIRD_PARTY_LOG_DIR / "zeal.log"),
        },
        "loggers": {
            "django": build_logger(["console", "django_file"]),
            "django.request": build_logger(["console", "django_request_file"], level=REQUEST_LOG_LEVEL),
            "django.db.backends": build_logger(["django_db_file"], level=DATABASE_LOG_LEVEL),
            "django.server": build_logger(["console", "django_server_file"]),
            "django.template": build_logger(["console", "django_templates_file"]),
            "django_safe_migrations": build_logger(["django_safe_migrations_file"]),
            "rest_framework": build_logger(["rest_framework_file"]),
            "axes": build_logger(["console_warnings", "axes_file"]),
            "silk": build_logger(["silk_file"]),
            "py.warnings": build_logger(["console"]),
            "zeal": build_logger(["zeal_file"]),
        },
        "root": {
            "handlers": ["root_file"],
            "level": DEFAULT_LOG_LEVEL,
        },
    }
