""" Settings for the application. """

import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class SiteSettings(BaseSettings):
    """Settings for the site."""

    host: str = Field(os.getenv("SITE_HOST"))
    port: int = Field(os.getenv("SITE_PORT"))
    loop: str = Field("asyncio")  # для асинхронного дебага
    log_level: str = Field(os.getenv("SITE_LOG_LEVEL"))
    reload: bool = Field(True)  # перезагрузка uvicorn
    reload_delay: float = Field(0.25)


class ApplicationSettings(BaseSettings):
    """Settings for the application."""

    title: str = Field("Fastapi with tortoise ORM template")
    description: str = Field("Шаблон приложения на tortoise ORM")
    debug: bool = Field(True)
    version: str = Field("0.1.0")


class DataBaseCredentials(BaseSettings):
    """Settings for the database."""

    db_user: str = Field(os.getenv("MYSQL_USER"))
    password: str = Field(os.getenv("MYSQL_PASSWORD"))
    port: str = Field(os.getenv("MYSQL_INTERNAL_PORT"))
    db_name: str = Field(os.getenv("MYSQL_DATABASE"))
    host: str = Field(os.getenv("MYSQL_HOST"))
    # host: str = Field("127.0.0.1")
    # host: str = Field("db")


class DataBaseConnections(BaseSettings):  # type: ignore
    """Settings for the database connections."""

    default: str = Field(
        "mysql://{db_user}:{password}@{host}:{port}/{db_name}".format(
            **DataBaseCredentials().model_dump()  # type: ignore
        )
    )


class DataBaseModels(BaseSettings):
    """Settings for the database models."""

    models: list[str] = Field(
        [
            "aerich.models",
        ]
    )


class DataBaseSettings(BaseSettings):
    """Settings for the database."""

    connections: dict = Field(DataBaseConnections().model_dump())  # type: ignore
    apps: dict = Field(
        {
            "models": DataBaseModels().model_dump(),  # type: ignore
        }
    )  # type: ignore


class TortoiseSettings(BaseSettings):
    """
    Settings for Tortoise ORM configuration.
    """

    generate_schemas: bool = Field(False)
    add_exception_handlers: bool = Field(True)

    # generate_schemas: bool = Field(True, env="TORTOISE_GENERATE_SCHEMAS")
    # add_exception_handlers: bool = Field(True, env="DATABASE_EXCEPTION_HANDLERS")


class AuthSettings(BaseSettings):
    """Represents JWT token settings."""

    type: str = Field("Bearer")
    password_time: int = Field(3)
    algorithm: str = Field("HS256")
    # expires: int = Field(int(os.getenv("TOKEN_EXPIRES")))  # 1 час
    expires: int = Field(60 * 60 * 24 * 7)  # 1 неделя
    hasher_deprecated: str = Field("auto")
    hasher_schemes: list[str] = Field(["bcrypt"])
    token_url: str = Field("users/login")

    secret_key: str = Field(os.getenv("AUTH_SECRET_KEY"))


class CORSSettings(BaseSettings):
    """Settings for the CORS."""

    allow_credentials: bool = Field(True)
    allow_methods: list[str] = Field(["*"])
    allow_headers: list[str] = Field(["*", "Authorization"])
    allow_origins: list[str] = Field(
        [
            "*",
        ]
    )


class SuperUsersSettings(BaseSettings):
    """Settings for the superusers."""

    superusers: list[str] = Field(
        [
            "tripspy_as_superuser",
        ]
    )


