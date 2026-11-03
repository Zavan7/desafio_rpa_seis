"""Configuração centralizada de logging da automação.

Define saída legível no console e arquivos JSON rotativos em logs/:
    app.log: Logs gerais da aplicação (INFO ou acima).
    database.log: Logs do logger "database".
    error.log: Somente erros (ERROR ou acima) de todos os loggers.
"""

import logging
import logging.config
from pathlib import Path

from pythonjsonlogger.json import JsonFormatter

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


class CustomJsonFormatter(JsonFormatter):
    """Formatter JSON que adiciona campos fixos a cada registro de log.

    Garante que todo log em arquivo traga nível, nome do logger, arquivo e
    linha de origem, facilitando a busca e o filtro dos registros.
    """

    def add_fields(self, log_record, record, message_dict):
        """Preenche os campos do registro JSON.

        Args:
            log_record(dict): Dicionário que será serializado em JSON.
            record(logging.LogRecord): Registro original do logging.
            message_dict(dict): Campos extras vindos da mensagem.
        """
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

    # Rede de segurança: qualquer logger sem configuração própria (main
    # importado pelo entry point ou por testes, services, utils) cai aqui
    # em vez de se perder.
    "root": {
        "handlers": [
            "console",
            "app_file",
            "error_file",
        ],
        "level": "INFO",
    },
}


def setup_logging() -> None:
    """Aplica a configuração LOGGING ao módulo logging.

    Deve ser chamada uma única vez, no início da execução, antes de
    qualquer log ser emitido.
    """
    logging.config.dictConfig(LOGGING)
