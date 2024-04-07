""" Configuration module. """
import os
from typing import Any

from config.settings import (
    ApplicationSettings,
    AuthSettings,
    CORSSettings,
    DataBaseSettings,
    SiteSettings,
    SuperUsersSettings,
    TortoiseSettings,
)

base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_config: dict[str, Any] = ApplicationSettings().model_dump()  # type: ignore
site_config: dict[str, Any] = SiteSettings().model_dump()  # type: ignore
cors_config: dict[str, Any] = CORSSettings().model_dump()  # type: ignore
auth_config: dict[str, Any] = AuthSettings().model_dump()  # type: ignore
super_users_config: dict[str, Any] = SuperUsersSettings().model_dump()  # type: ignore
database_config: dict[str, Any] = DataBaseSettings().model_dump()  # type: ignore
tortoise_config: dict[str, Any] = TortoiseSettings().model_dump()  # type: ignore
