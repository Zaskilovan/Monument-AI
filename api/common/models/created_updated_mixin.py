"""Содержит в себе миксин для создания полей 'created_at' и 'updated_at'."""
from datetime import datetime

from tortoise import fields


class TimeBasedMixin:
    """Создать поля 'created_at' и 'updated_at' для модели."""

    created_at: datetime = fields.DatetimeField(description="Дата создания", auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(description="Дата обновления", auto_now=True)
