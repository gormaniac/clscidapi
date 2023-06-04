"""The Uvicorn runner for the app."""

import uvicorn

from . import api
from . import CONF


if __name__ == "__main__":
    uvicorn.run(
        api.app,
        host=CONF.host,
        port=CONF.port,
        ssl_certfile=CONF.ssl_certfile,
        ssl_keyfile=CONF.ssl_keyfile,
        log_config=CONF.log_config,
        log_level=CONF.log_level,
    )
