"""To init/migrate db and star app."""

import os
import subprocess

from config import site_config
from config.app import get_fastapi_app

app = get_fastapi_app()
command = [
    "aerich",
    "-c",
    "../pyproject.toml",
]
init_aerich_conf_files_arguments = [
    "init",
    "-t",
    "config.database_config",
    "--location",
    "../migrations",
]
init_db_arguments = [
    "init-db",
]
migrate_tables_arguments = [
    "migrate",
]
upgrade_tables_arguments = [
    "upgrade",
]

if os.path.exists("../migrations"):
    subprocess.run(command + migrate_tables_arguments)
    subprocess.run(command + upgrade_tables_arguments)
else:
    subprocess.run(command + init_aerich_conf_files_arguments)
    subprocess.run(command + init_db_arguments)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run:app", **site_config)
