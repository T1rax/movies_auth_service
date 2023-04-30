from core.config import configs
from logging import config as logging_config


LOG_FORMAT = (
    "%(asctime)s - %(module)-10s - %(funcName)-20s - %(levelname)-5s - %(message)s"
)
LOG_DEFAULT_HANDLERS = ["console"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}


def set_up_logging():
    # Применяем настройки логирования
    logging_config.dictConfig(LOGGING)
