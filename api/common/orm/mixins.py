from typing import Any, Iterable, Optional

from tortoise import Model
from tortoise.expressions import Q
from tortoise.functions import Count
from tortoise.query_utils import Prefetch
from tortoise.queryset import ExistsQuery, QuerySet, QuerySetSingle, RawSQLQuery


class BaseMixin:
    """
    Базовый миксин
    """

    model: Model


class ExecuteMixin(BaseMixin):
    """
    Выполнение сырого SQL запроса(RAW SQL)
    """

    async def execute(self, raw_sql: str) -> list[RawSQLQuery]:
        return await self.model.raw(raw_sql)


class CreateMixin(BaseMixin):
    """
    Миксин создания модели
    """

    async def create(self, data: dict) -> "CreateMixin.model":  # type: ignore
        return await self.model.create(**data)


class RetrieveMixin(BaseMixin):
    """
    Миксин получения модели
    """

    def retrieve(
        self,
        filters: dict[str, Any],
        q_filters: Optional[Iterable[Q]] = None,
        annotations: Optional[dict] = None,
        related_fields: Optional[list[str]] = None,
        prefetch_fields: Optional[list[str | dict[str, Any]]] = None,
        ordering: Optional[str] = None,
    ) -> QuerySetSingle["RetrieveMixin.model"]:  # type: ignore
        model: QuerySet[Model] = self.model.filter(**filters)

        if q_filters:
            model: QuerySet[Model] = model.filter(*q_filters)  # type: ignore
        if related_fields:
            model: QuerySet[Model] = model.select_related(*related_fields)  # type: ignore
        if prefetch_fields:
            prefetches: list[str | Prefetch] = []
            for prefetch in prefetch_fields:
                if isinstance(prefetch, str):
                    prefetches.append(prefetch)
                else:
                    prefetches.append(Prefetch(**prefetch))
            model: QuerySet[Model] = model.prefetch_related(*prefetches)  # type: ignore
        if annotations:
            model: QuerySet[Model] = model.annotate(**annotations)  # type: ignore
        if ordering:
            model: QuerySet[Model] = model.order_by(ordering)  # type: ignore

        model: QuerySetSingle[Model] = model.first()  # type: ignore

        return model  # type: ignore


class ListMixin(BaseMixin):
    """
    Миксин списка моделей
    """

    def list(
        self,
        end: Optional[int] = None,
        start: Optional[int] = None,
        ordering: Optional[str] = None,
        q_filters: Optional[Iterable[Q]] = None,
        filters: Optional[dict[str, Any]] = None,
        related_fields: Optional[list[str]] = None,
        annotations: Optional[dict[str, Any]] = None,
        prefetch_fields: Optional[list[str | dict[str, Any]]] = None,
        exclude: Optional[dict[str, Any]] = None,
    ) -> QuerySet["ListMixin.model"]:  # type: ignore
        models: QuerySet[Model] = self.model.all()

        if filters:
            models: QuerySet[Model] = models.filter(**filters)  # type: ignore
        if q_filters:
            models: QuerySet[Model] = models.filter(*q_filters)  # type: ignore
        if exclude:
            models: QuerySet[Model] = models.exclude(**exclude)  # type: ignore
        if related_fields:
            models: QuerySet[Model] = models.select_related(*related_fields)  # type: ignore
        if prefetch_fields:
            prefetches: list[str | Prefetch] = []
            for prefetch in prefetch_fields:
                if isinstance(prefetch, str):
                    prefetches.append(prefetch)
                else:
                    prefetches.append(Prefetch(**prefetch))

            models: QuerySet[Model] = models.prefetch_related(*prefetches)  # type: ignore

        if annotations:
            models: QuerySet[Model] = models.annotate(**annotations)  # type: ignore
        if start and end:
            models: QuerySet[Model] = models.offset(start).limit(end - start)  # type: ignore
        if ordering:
            models: QuerySet[Model] = models.order_by(ordering)  # type: ignore
        return models


class UpdateMixin(BaseMixin):
    """
    Миксин обновления модели
    """

    async def update(self, model: Model, data: dict) -> "UpdateMixin.model":  # type: ignore
        for field, value in data.items():
            setattr(model, field, value)
        await model.save()
        return model


class UpdateOrCreateMixin(BaseMixin):
    """
    Миксин создания или обновления модели
    """

    async def create_or_update(self, filters: dict, data: dict) -> Model:
        model, _ = await self.model.update_or_create(**filters, defaults=data)
        return model


class DeleteMixin(BaseMixin):
    """
    Миксин удаления модели
    """

    async def delete(self, model: Model) -> None:
        await model.delete()


class BulkUpdateMixin(BaseMixin):
    """
    Миксин массового обновления
    """

    async def bulk_update(self, data: dict, filters: dict) -> None:
        qs: QuerySet[Model] = self.model.select_for_update().filter(**filters)
        await qs.update(**data)


class ExistsMixin(BaseMixin):
    """
    Миксин проверки существования модели
    """

    def exists(self, filters: dict) -> ExistsQuery:
        models: ExistsQuery = self.model.filter(**filters).exists()
        return models


class CountMixin(BaseMixin):
    """
    Миксин количества моделей
    """

    async def count(self, filters: Optional[dict] = None, q_filters: Optional[Iterable[Q]] = None) -> int:
        """
        Количество агентов
        """

        models: QuerySet[Model] = self.model.all()

        if filters:
            models: QuerySet[Model] = models.filter(**filters)  # type: ignore
        if q_filters:
            models: QuerySet[Model] = models.filter(*q_filters)  # type: ignore
        count: int = await models.annotate(count=Count("id", distinct=True)).count()
        return count


class ReadOnlyMixin(ListMixin, RetrieveMixin, ExistsMixin):
    """
    Миксин репозиториев только для чтения
    """


class WriteOnlyMixin(CreateMixin, UpdateMixin, UpdateOrCreateMixin, BulkUpdateMixin):
    """
    Миксин репозиториев только для записи
    """


class ReadWriteMixin(ReadOnlyMixin, WriteOnlyMixin):
    """
    Миксин репозиториев чтения и записи
    """


class CRUDMixin(ReadWriteMixin, DeleteMixin):
    """
    Миксин CRUD
    """


class GenericMixin(CRUDMixin, CountMixin):
    """
    Все миксины
    """


class TimeBasedMixin:
    ...
