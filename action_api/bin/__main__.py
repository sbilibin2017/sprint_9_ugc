import logging

import libs.app.app as app_module
import libs.app.config as app_config
import uvicorn

logger = logging.getLogger(__name__)

app_instance = app_module.Application()
app = app_instance.create_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app_config.base_settings.server_host,
        port=app_config.base_settings.server_port,
    )
