import logging.config as logging_config
import pathlib

import libs.app.logger as logger_config
import libs.app.settings as settings

BASE_PATH = pathlib.Path(__file__).parent.parent.parent
ENV_PATH = BASE_PATH / ".env"

logging_config.dictConfig(logger_config.LOGGING)

base_settings = settings.BaseSettings(_env_file=ENV_PATH)  # type: ignore[reportGeneralTypeIssues]
mongo_settings = settings.MongoSettings(_env_file=ENV_PATH)  # type: ignore[reportGeneralTypeIssues]
auth_settings = settings.AuthSettings(_env_file=ENV_PATH)  # type: ignore[reportGeneralTypeIssues]
