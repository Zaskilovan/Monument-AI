"""Содержит функцию для возврата списка роутеров."""
from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    """Возвращает список роутеров."""
    routers: list[APIRouter] = list()

    # from src.admins.api import admins_router
    # routers.append(admins_router)


    return routers


"""Содержит функцию для возврата списка роутеров."""
