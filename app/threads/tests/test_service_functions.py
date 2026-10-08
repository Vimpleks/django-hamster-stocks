import pytest

from threads.models import StockThread, Thread
from threads.services import get_quantity_color_in_storage, get_quantity_thread_in_storage, filter_by_field, \
    add_thread_in_storage
from threads.templatetags.threads_tags import remove_trailing_zeros


@pytest.mark.parametrize("value,expected", [
    (None, ""),
    ("0", "0"),
    ("5", "5"),
    ("3.00", "3"),
    ("3.10", "3.1"),
    ("3.1400", "3.14"),
    ("10.000", "10"),
    ("0.500", "0.5"),
    ("0.050", "0.05"),
    ("123.456000", "123.456"),
    (0, "0"),
    (5, "5"),
    (3.0, "3"),
    (3.1, "3.1"),
    (10.0, "10"),
    (0.5, "0.5"),
])
def test_remove_trailing_zeros_valid_cases(value, expected):
    # Assert
    assert remove_trailing_zeros(value) == expected


def test_get_quantity_color_in_storage_returns_correct_count_for_filled_stock(some_stock_threads, stock):
    # Act
    result = get_quantity_color_in_storage(
        instance=stock,
        model=StockThread,
        related_field="stock",
    )

    # Assert
    assert result == 2


def test_get_quantity_color_in_storage_empty_stock_returns_zero(stock):
    # Act
    result = get_quantity_color_in_storage(
        instance=stock,
        model=StockThread,
        related_field="stock",
    )

    # Assert
    assert result == 0


def test_get_quantity_thread_in_storage_returns_correct_count_for_filled_stock(some_stock_threads, stock):
    # Act
    result = get_quantity_thread_in_storage(
        instance=stock,
        model=StockThread,
        related_field="stock",
    )

    # Assert
    assert result == 3.5


def test_get_quantity_thread_in_storage_empty_stock_returns_zero(stock):
    # Act
    result = get_quantity_thread_in_storage(
        instance=stock,
        model=StockThread,
        related_field="stock",
    )

    # Assert
    assert result == 0


def test_filter_by_field_applies_filter_when_value_present(first_thread, second_thread):
    # Arrange
    query_set = Thread.objects.all()

    # Act
    filtered_query_set = filter_by_field(query_set, 'B5200', 'article')

    # Assert
    assert filtered_query_set.count() == 1
    assert filtered_query_set.first().article == 'B5200'


def test_filter_by_field_returns_original_queryset_when_filter_value_empty_string(first_thread, second_thread):
    # Arrange
    query_set = Thread.objects.all()

    # Act
    filtered_query_set = filter_by_field(query_set, '', 'article')

    # Assert
    assert filtered_query_set.count() == 2
    assert set(query_set.values_list('id', flat=True)) == set(filtered_query_set.values_list('id', flat=True))


def test_filter_by_field_works_with_icontains_lookup(first_thread, second_thread):
    # Arrange
    query_set = Thread.objects.all()

    # Act
    filtered_query_set = filter_by_field(query_set, 'B520', 'article__icontains')

    # Assert
    assert filtered_query_set.count() == 1
    assert filtered_query_set.first().article == 'B5200'


def test_add_thread_in_storage_creates_new_record_when_not_exists(stock, first_thread):
    # Arrange
    initial_count = StockThread.objects.count()

    # Act
    add_thread_in_storage(
        storage=StockThread,
        quantity=3.5,
        thread=first_thread,
        lookup_field='stock',
        filter_value=stock,
    )

    # Assert
    assert StockThread.objects.count() == initial_count + 1
    assert StockThread.objects.get(stock=stock, thread=first_thread).quantity == 3.5


def test_add_thread_in_storage_increases_quantity_when_exists(stock, first_thread, first_stock_thread):
    # Act
    add_thread_in_storage(
        storage=StockThread,
        quantity=3.5,
        thread=first_thread,
        lookup_field='stock',
        filter_value=stock,
    )

    # Assert
    assert StockThread.objects.get(stock=stock, thread=first_thread).quantity == 4.5
