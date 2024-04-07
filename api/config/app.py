from fastapi import FastAPI


def get_fastapi_app() -> FastAPI:
    from config.initializers import (  # init_redis,
        init_app,
        init_cors,
        init_database,
        init_exception_handlers,
        init_pagination,
        init_routers,
    )

    application: FastAPI = init_app()

    init_cors(application)
    init_routers(application)
    init_database(application)
    init_exception_handlers(application)
    init_pagination(application)
    # init_redis()

    return application
