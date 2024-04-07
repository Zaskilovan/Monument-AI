from fastapi import FastAPI


def init_app() -> FastAPI:
    from config import app_config

    app = FastAPI(**app_config)
    return app


def init_cors(application: FastAPI) -> None:
    from config import cors_config
    from fastapi.middleware.cors import CORSMiddleware

    application.add_middleware(CORSMiddleware, **cors_config)


def init_routers(application: FastAPI) -> None:
    from config.routers import get_routers

    for router in get_routers():
        application.include_router(router)


def init_database(application: FastAPI) -> None:
    from config import database_config, tortoise_config
    from tortoise.contrib.fastapi import register_tortoise

    register_tortoise(application, config=database_config, **tortoise_config)


def init_exception_handlers(application: FastAPI) -> None:
    from common.exceptions.base import BaseHTTPException
    from common.handlers import common_exception_handler

    application.add_exception_handler(BaseHTTPException, common_exception_handler)


def init_pagination(application: FastAPI) -> None:
    from fastapi_pagination import add_pagination

    add_pagination(application)


