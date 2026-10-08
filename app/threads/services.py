from django.db.models import Count, Sum, Model
from django.db.models.query import QuerySet
from typing import Type

from .models import Thread


def get_quantity_color_in_storage(instance: Model, model: Type[Model], related_field: str) -> int:
    """
    Возвращает количество цветов (уникальных артикулов) ниток в хранилище.

    :param instance: экземпляр модели хранилища (Stock, Basket и т.п.)
    :param model: модель связи хранилища с нитками (StockThread, BasketThread и т.п.)
    :param related_field: имя поля FK в модели связи хранилища с нитками (например, 'stock', 'basket')
    """
    result = model.objects.filter(**{related_field: instance}).aggregate(count=Count('thread'))['count']
    return result if result is not None else 0


def get_quantity_thread_in_storage(instance: Model, model: Type[Model], related_field: str) -> int | float:
    """
    Возвращает количество мотков ниток в хранилище.

    :param instance: экземпляр модели хранилища (Stock, Basket и т.п.)
    :param model: модель связи хранилища с нитками (StockThread, BasketThread и т.п.)
    :param related_field: имя поля FK в модели связи хранилища с нитками (например, 'stock', 'basket')
    """
    result = model.objects.filter(**{related_field: instance}).aggregate(sum=Sum('quantity'))['sum']
    return round(result, 2) if result is not None else 0


def filter_by_field(queryset: QuerySet, filter_value: str, lookup_field: str) -> QuerySet:
    """
    Фильтрует queryset по полю lookup_field.

    :param queryset: Исходный queryset для фильтрации.
    :param filter_value: Значение для поиска в поле lookup_field (может быть None).
    :param lookup_field: Значения для поля фильтрации.
    :return: Отфильтрованный queryset. Если filter_value пустое, возвращает исходный queryset без изменений.
    """
    if filter_value:
        return queryset.filter(**{lookup_field: filter_value})
    return queryset


def add_thread_in_storage(storage: Type[Model], quantity: float, thread: Model, lookup_field: str, filter_value: Model) -> None:
    """
    Функция добавляет нитку в хранилище. Если нитка в хранилище есть, то увеличивает ее количество на quantity.

    :param storage: модель связи хранилища с нитками (StockThread, BasketThread и т.п.)
    :param quantity: количество мотков нитки для добавления
    :param thread: экземпляр модели нитки, которую надо добавить
    :param lookup_field: имя поля FK в модели связи хранилища с нитками (например, 'stock', 'basket')
    :param filter_value: экземпляр модели хранилища (Stock, Basket и т.п.)
    """
    try:
        storage_thread = storage.objects.get(**{lookup_field: filter_value}, thread=thread)
        quantity_add = storage_thread.quantity + quantity
        storage_thread.quantity = quantity_add
        storage_thread.save(update_fields=['quantity'])
    except storage.DoesNotExist:
        storage.objects.create(**{lookup_field: filter_value}, thread=thread, quantity=quantity)
