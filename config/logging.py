import logging
import logging.config
from pathlib import Path

from pythonjsonlogger.json import JsonFormatter


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["file"] = record.filename
        log_record["line"] = record.lineno


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s -> %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },

        "json": {
            "()": CustomJsonFormatter,
            "format": (
                "%(asctime)s %(levelname)s %(name)s "
                "%(filename)s %(lineno)d %(message)s"
            ),
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
        },

        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        },

        "db_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": str(LOG_DIR / "database.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        },

        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": str(LOG_DIR / "error.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },

    "loggers": {
        # Logs da aplicação
        "pages": {
            "handlers": [
                "console",
                "app_file",
                "error_file",
            ],
            "level": "DEBUG",
            "propagate": False,
        },

        "validation": {
            "handlers": [
                "console",
                "app_file",
                "error_file",
            ],
            "level": "DEBUG",
            "propagate": False,
        },

        "__main__": {
            "handlers": [
                "console",
                "app_file",
                "error_file",
            ],
            "level": "DEBUG",
            "propagate": False,
        },

        # Logs do banco
        "database": {
            "handlers": [
                "db_file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },

        # Bibliotecas externas
        "pymongo": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },

        "asyncio": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
    },

    "root": {
        "handlers": [],
        "level": "WARNING",
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING)