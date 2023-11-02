# -*- coding: utf-8 -*-
import uvicorn

from application import app
from utils.config import Config


def make_server():
    uvicorn_config = uvicorn.Config(
        app=app,
        host=Config.get("http.host"),
        port=Config.get("http.port"),
        log_level=Config.get("http.log-level"),
        access_log=Config.get("http.access-log"),
    )
    return uvicorn.Server(config=uvicorn_config)


def serve():
    server = make_server()
    server.run()


if __name__ == "__main__":
    serve()
