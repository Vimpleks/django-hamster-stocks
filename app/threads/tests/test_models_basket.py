import pytest

from threads.models import Basket, BasketThread
from django.db import IntegrityError


def test_create_basket_and_user_relationship(user):
    # Act
    basket = Basket.objects.create(owner=user)

    # Assert
    assert basket.owner == user
    assert basket.id is not None


def test_basket_user_cascade_delete(user, basket):
    # Act
    user.delete()

    # Assert
    assert not Basket.objects.filter(id=basket.id).exists()


def test_basket_str(basket):
    # Assert
    assert str(basket) == f'{basket.id} - testuser'


def test_create_basket_thread(basket, first_thread):
    # Act
    basket_thread = BasketThread.objects.create(basket=basket, thread=first_thread, quantity=1.5)

    # Assert
    assert basket_thread.quantity == 1.5
    assert basket_thread.id is not None


def test_basket_thread_basket_relationship(first_basket_thread, basket):
    # Assert
    assert first_basket_thread.basket == basket


def test_basket_thread_thread_relationship(first_basket_thread, first_thread):
    # Assert
    assert first_basket_thread.thread == first_thread


def test_basket_thread_basket_cascade_delete(first_basket_thread, basket):
    # Act
    basket.delete()

    # Assert
    assert not BasketThread.objects.filter(id=first_basket_thread.id).exists()


def test_basket_thread_thread_cascade_delete(first_basket_thread, first_thread):
    # Act
    first_thread.delete()

    # Assert
    assert not BasketThread.objects.filter(id=first_basket_thread.id).exists()


def test_basket_thread_unique(first_basket_thread, basket, first_thread):
    # Assert
    with pytest.raises(IntegrityError):
        BasketThread.objects.create(basket=basket, thread=first_thread, quantity=2)


def test_basket_thread_rejects_negative_quantity(basket, first_thread):
    with pytest.raises(IntegrityError):
        BasketThread.objects.create(
            basket=basket,
            thread=first_thread,
            quantity=-10,
        )


def test_basket_thread_rejects_zero_quantity(basket, first_thread):
    with pytest.raises(IntegrityError):
        BasketThread.objects.create(
            basket=basket,
            thread=first_thread,
            quantity=0,
        )


def test_basket_thread_rejects_very_small_quantity(basket, first_thread):
    with pytest.raises(IntegrityError):
        BasketThread.objects.create(
            basket=basket,
            thread=first_thread,
            quantity=0.001,
        )
