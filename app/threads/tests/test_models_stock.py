import pytest

from threads.models import Stock, StockThread
from django.db import IntegrityError


def test_create_stock_and_user_relationship(user):
    # Act
    stock = Stock.objects.create(owner=user)

    # Assert
    assert stock.owner == user
    assert stock.id is not None


def test_stock_user_cascade_delete(user, stock):
    # Act
    user.delete()

    # Assert
    assert not Stock.objects.filter(id=stock.id).exists()


def test_stock_str(stock):
    # Assert
    assert str(stock) == f'{stock.id} - testuser'


def test_create_stock_thread(stock, first_thread):
    # Act
    stock_thread = StockThread.objects.create(stock=stock, thread=first_thread, quantity=1.5)

    # Assert
    assert stock_thread.quantity == 1.5
    assert stock_thread.id is not None


def test_stock_thread_stock_relationship(first_stock_thread, stock):
    # Assert
    assert first_stock_thread.stock == stock


def test_stock_thread_thread_relationship(first_stock_thread, first_thread):
    # Assert
    assert first_stock_thread.thread == first_thread


def test_stock_thread_stock_cascade_delete(first_stock_thread, stock):
    # Act
    stock.delete()

    # Assert
    assert not StockThread.objects.filter(id=first_stock_thread.id).exists()


def test_stock_thread_thread_cascade_delete(first_stock_thread, first_thread):
    # Act
    first_thread.delete()

    # Assert
    assert not StockThread.objects.filter(id=first_stock_thread.id).exists()


def test_stock_thread_unique(first_stock_thread, stock, first_thread):
    # Assert
    with pytest.raises(IntegrityError):
        StockThread.objects.create(stock=stock, thread=first_thread, quantity=2)


def test_stock_thread_rejects_negative_quantity(stock, first_thread):
    with pytest.raises(IntegrityError):
        StockThread.objects.create(
            stock=stock,
            thread=first_thread,
            quantity=-10,
        )


def test_stock_thread_rejects_zero_quantity(stock, first_thread):
    with pytest.raises(IntegrityError):
        StockThread.objects.create(
            stock=stock,
            thread=first_thread,
            quantity=0,
        )


def test_stock_thread_rejects_very_small_quantity(stock, first_thread):
    with pytest.raises(IntegrityError):
        StockThread.objects.create(
            stock=stock,
            thread=first_thread,
            quantity=0.001,
        )
