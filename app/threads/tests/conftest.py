import pytest
from django.contrib.auth.models import User

from threads.models import Thread, Manufacturer, Stock, StockThread, Basket, BasketThread, Project, ProjectThread


@pytest.fixture
def manufacturer(db):
    return Manufacturer.objects.create(name='DMC', slug='dmc')


@pytest.fixture
def first_thread(manufacturer):
    return Thread.objects.create(
        article='310',
        name='Black',
        manufacturer=manufacturer,
    )


@pytest.fixture
def second_thread(manufacturer):
    return Thread.objects.create(
        article='B5200',
        name='White',
        manufacturer=manufacturer,
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='test-password-123',
        first_name='Иван',
        last_name='Петров',
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='another_user',
        password='test-password-123',
        first_name='Петр',
        last_name='Иванов',
    )


@pytest.fixture
def logged_in_client(client, user):
    client.login(username='testuser', password='test-password-123')
    return client, user


@pytest.fixture
def stock(user):
    return Stock.objects.create(owner=user)


@pytest.fixture
def first_stock_thread(stock, first_thread):
    return StockThread.objects.create(stock=stock, thread=first_thread, quantity=1)


@pytest.fixture
def some_stock_threads(stock, first_thread, second_thread):
    return [
        StockThread.objects.create(stock=stock, thread=first_thread, quantity=1.5),
        StockThread.objects.create(stock=stock, thread=second_thread, quantity=2),
    ]


@pytest.fixture
def another_stock(another_user):
    return Stock.objects.create(owner=another_user)


@pytest.fixture
def another_stock_thread(another_stock, first_thread):
    return StockThread.objects.create(stock=another_stock, thread=first_thread, quantity=1)


@pytest.fixture
def basket(user):
    return Basket.objects.create(owner=user)


@pytest.fixture
def first_basket_thread(basket, first_thread):
    return BasketThread.objects.create(basket=basket, thread=first_thread, quantity=1)


@pytest.fixture
def some_basket_threads(basket, first_thread, second_thread):
    return [
        BasketThread.objects.create(basket=basket, thread=first_thread, quantity=1.5),
        BasketThread.objects.create(basket=basket, thread=second_thread, quantity=2),
    ]


@pytest.fixture
def another_basket(another_user):
    return Basket.objects.create(owner=another_user)


@pytest.fixture
def another_basket_thread(another_basket, first_thread):
    return BasketThread.objects.create(basket=another_basket, thread=first_thread, quantity=1)


@pytest.fixture
def project(user):
    return Project.objects.create(
        name='Акварельные домики',
        description='Похожи на норвежские домики',
        designer='Наталья Юркевич',
        status='kitted',
        owner=user,
    )


@pytest.fixture
def another_project(another_user, project):
    return Project.objects.create(
        name='Акварельные домики',
        description='Похожи на норвежские домики',
        designer='Наталья Юркевич',
        status='kitted',
        owner=another_user,
    )


@pytest.fixture
def first_project_thread(project, first_thread):
    return ProjectThread.objects.create(project=project, thread=first_thread, quantity=1)


@pytest.fixture
def another_project_thread(another_project, first_thread):
    return ProjectThread.objects.create(project=another_project, thread=first_thread, quantity=1)
