import pytest

from threads.models import Manufacturer, Thread
from django.db import IntegrityError, DataError


def test_create_manufacturer(db):
    # Act
    manufacturer = Manufacturer.objects.create(name='Gamma', slug='gamma')

    # Assert
    assert manufacturer.name == 'Gamma'
    assert manufacturer.slug == 'gamma'
    assert manufacturer.id is not None


def test_manufacturer_name_max_length(db):
    # Assert
    with pytest.raises(DataError):
        Manufacturer.objects.create(name='g' * 51, slug='gamma')


def test_manufacturer_name_unique(manufacturer):
    # Assert
    with pytest.raises(IntegrityError):
        Manufacturer.objects.create(name='DMC', slug='gamma')


def test_manufacturer_slug_unique(manufacturer):
    # Assert
    with pytest.raises(IntegrityError):
        Manufacturer.objects.create(name='Gamma', slug='dmc')


def test_manufacturer_str(manufacturer):
    # Assert
    assert str(manufacturer) == 'DMC'


def test_create_thread(manufacturer):
    # Act
    thread = Thread.objects.create(
        article='310',
        name='Black',
        manufacturer=manufacturer,
    )

    # Assert
    assert thread.article == '310'
    assert thread.name == 'Black'
    assert thread.manufacturer.name == 'DMC'
    assert thread.id is not None


def test_thread_article_max_length(manufacturer):
    # Assert
    with pytest.raises(DataError):
        Thread.objects.create(article='g' * 51, manufacturer=manufacturer)


def test_thread_name_max_length(manufacturer):
    # Assert
    with pytest.raises(DataError):
        Thread.objects.create(article='310', name='B' * 101, manufacturer=manufacturer)


def test_thread_article_manufacturer_unique(second_thread, manufacturer):
    # Assert
    with pytest.raises(IntegrityError):
        Thread.objects.create(article='B5200', manufacturer=manufacturer)


def test_thread_str(second_thread):
    # Assert
    assert str(second_thread) == 'DMC B5200'


def test_thread_manufacturer_relationship(first_thread, manufacturer):
    # Assert
    assert first_thread.manufacturer == manufacturer


def test_thread_manufacturer_cascade_delete(first_thread, second_thread, manufacturer):
    # Act
    manufacturer.delete()

    # Assert
    assert not Thread.objects.filter(id=first_thread.id).exists()
    assert not Thread.objects.filter(id=second_thread.id).exists()
