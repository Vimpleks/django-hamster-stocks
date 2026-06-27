from threads.forms import ThreadQuantityForm, ThreadUpdateStockForm, ThreadUpdateBasketForm, ThreadUpdateProjectForm, \
    ProjectForm
from threads.models import StockThread, BasketThread, ProjectThread


def test_thread_quantity_form_valid_data():
    data = {
        "quantity": 10.5,
        "thread": 2,
    }
    form = ThreadQuantityForm(data=data)
    assert form.is_valid() is True
    assert form.cleaned_data["quantity"] == 10.5
    assert form.cleaned_data["thread"] == 2


def test_thread_updates_tock_form_valid_data(first_stock_thread):
    # Arrange
    data = {"quantity": 2.5}
    form = ThreadUpdateStockForm(data=data, instance=first_stock_thread)

    # Act
    instance = form.save()

    # Assert
    assert form.is_valid() is True
    assert instance.pk == first_stock_thread.pk
    assert instance.quantity == 2.5
    assert StockThread.objects.get(pk=first_stock_thread.pk).quantity == 2.5


def test_thread_update_basket_form_valid_data(first_basket_thread):
    # Arrange
    data = {"quantity": 3.5}
    form = ThreadUpdateBasketForm(data=data, instance=first_basket_thread)

    # Act
    instance = form.save()

    # Assert
    assert form.is_valid() is True
    assert instance.pk == first_basket_thread.pk
    assert instance.quantity == 3.5
    assert BasketThread.objects.get(pk=first_basket_thread.pk).quantity == 3.5


def test_thread_update_project_form_valid_data(first_project_thread):
    # Arrange
    data = {"quantity": 4.5}
    form = ThreadUpdateProjectForm(data=data, instance=first_project_thread)

    # Act
    instance = form.save()

    # Assert
    assert form.is_valid() is True
    assert instance.pk == first_project_thread.pk
    assert instance.quantity == 4.5
    assert ProjectThread.objects.get(pk=first_project_thread.pk).quantity == 4.5


def test_project_form_valid_create(user):
    # Arrange
    data = {
        'name': 'Акварельные домики',
        'description': 'Похожи на норвежские домики',
        'designer': 'Наталья Юркевич',
        'status': 'kitted',
        'owner': user,
    }
    form = ProjectForm(data=data)

    # Act
    instance = form.save()

    assert form.is_valid() is True
    assert instance.name == 'Акварельные домики'
    assert instance.description == 'Похожи на норвежские домики'
    assert instance.designer == 'Наталья Юркевич'
    assert instance.status == 'kitted'
    assert instance.owner == user


def test_valid_update(project, user):
    # Arrange
    data = {
        'name': 'Домики',
        'status': 'in progress',
        'owner': user,
    }
    form = ProjectForm(data=data, instance=project)

    # Act
    instance = form.save()

    # Assert
    assert form.is_valid() is True
    assert instance.pk == project.pk
    assert instance.name == 'Домики'
    assert instance.status == 'in progress'
