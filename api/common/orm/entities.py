from .annotations import AnnotationBuilder
from .filters import QBuilder


class BaseRepo:
    """
    Базовый репозиторий
    """

    q_builder: QBuilder
    a_builder: AnnotationBuilder
