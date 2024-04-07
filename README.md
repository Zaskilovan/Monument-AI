# Monument-AI


# Инициализация проекта:

```
git init .

git remote add origin https://{TOKEN}@github.com/MonumentAi/API.git

git pull origin main

poetry shell

poetry install

sudo service mysql start

sudo docker compose --env-file .env up -d

cd api

aerich -c ../pyproject.toml init -t config.database_config --location ../migrations

aerich -c ../pyproject.toml init-db

python3 -B run.py

```

# Обновление бд 

```

aerich -c ../pyproject.toml migrate

aerich -c ../pyproject.toml upgrade


```

## Линтеры

Для инициализации pre-commit использовать команду:
```
pre-commit install
```

После установки библиотек из poetry включая группу dev - необходимо удостовериться что VsCode Workspace инициализировал файл .vscode/settings.json.

После этого IDE будет подсвечивать проверки flake8, flake8-docstring, isort.

А при попытке сделать коммит не исправив все ошибки - pre-commit сделает это самостоятельно для black и isort, но с flake8 необходимо будет самостоятельно исправить все недочёты.