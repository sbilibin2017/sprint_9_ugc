import pydantic
import pydantic_settings


class LoggingSettings(pydantic_settings.BaseSettings):
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_default_handlers: list[str] = [
        "console",
    ]

    log_level_handlers: str = pydantic.Field(
        default="DEBUG", alias="LOG_LEVEL_HANDLERS"
    )
    log_level_loggers: str = pydantic.Field(default="INFO", alias="LOG_LEVEL_LOGGERS")
    log_level_root: str = pydantic.Field(default="INFO", alias="LOG_LEVEL_ROOT")


log_settings = LoggingSettings()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": log_settings.log_format},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": log_settings.log_level_handlers,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": log_settings.log_default_handlers,
            "level": log_settings.log_level_loggers,
        },
        "uvicorn.error": {
            "level": log_settings.log_level_loggers,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": log_settings.log_level_loggers,
            "propagate": False,
        },
    },
    "root": {
        "level": log_settings.log_level_root,
        "formatter": "verbose",
        "handlers": log_settings.log_default_handlers,
    },
}
