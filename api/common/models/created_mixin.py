"""Содержит в себе миксин для создания поля 'created_at'."""
from datetime import datetime

from tortoise import fields


class CreateTimeBasedMixin:
    """Создать поле 'created_at' для модели."""

    created_at: datetime = fields.DatetimeField(description="Дата создания", auto_now_add=True)
