from django.urls import reverse

from threads.forms import ThreadQuantityForm, ThreadUpdateBasketForm
from threads.models import BasketThread


def test_basket_authenticated_user(logged_in_client, some_basket_threads):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:basket'))

    # Assert
    assert response.status_code == 200
    assert response.context['title'] == 'Запасы хомяка - Список покупок'
    assert list(response.context['basket_threads']) == list(some_basket_threads)
    assert 'total_color' in response.context
    assert 'total_quantity' in response.context
    assert response.context['filter_value'] is None


def test_basket_unauthenticated_redirects(client):
    # Act
    response = client.get(reverse('threads:basket'), follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_basket_filters_by_article(logged_in_client, some_basket_threads):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:basket'), {'article': 'B5200'})

    # Assert
    assert response.status_code == 200
    assert response.context['basket_threads'].count() == 1
    assert response.context['basket_threads'].first().thread.article == 'B5200'
    assert response.context['filter_value'] == 'B5200'


def test_add_thread_basket_authenticated_user(logged_in_client, manufacturer, first_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_basket',
                          kwargs={'manufacturer_slug': manufacturer.slug}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - Нитки')
    assert response.context['manufacturer'] == manufacturer
    assert list(response.context['threads']) == [first_thread]
    assert response.context['filter_value'] is None
    assert isinstance(response.context['form'], ThreadQuantityForm)


def test_add_thread_basket_unauthenticated_redirects(client, manufacturer):
    # Act
    response = client.get(reverse('threads:add_thread_basket',
                          kwargs={'manufacturer_slug': manufacturer.slug}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_add_thread_basket_filters_by_article(logged_in_client, manufacturer, first_thread, second_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_basket',
                          kwargs={'manufacturer_slug': manufacturer.slug}),
                          {'article': 'B5200'})

    # Assert
    assert response.status_code == 200
    assert response.context['threads'].count() == 1
    assert response.context['threads'].first().article == 'B5200'
    assert response.context['filter_value'] == 'B5200'


def test_add_thread_basket_post_success(logged_in_client, manufacturer, second_thread, basket):
    # Arrange
    client, user = logged_in_client
    data = {
        'thread': second_thread.id,
        'quantity': 5.5,
    }

    # Act
    response = client.post(reverse('threads:add_thread_basket',
                           kwargs={'manufacturer_slug': manufacturer.slug}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:basket') in response.url
    assert BasketThread.objects.filter(
        basket=basket,
        thread=second_thread,
        quantity=5.5
    ).exists()


def test_add_thread_basket_invalid_slug_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_basket',
                                  kwargs={'manufacturer_slug': 'nonexistent-slug'}))

    # Assert
    assert response.status_code == 404


def test_update_thread_basket_authenticated_user(logged_in_client, first_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_basket',
                                  kwargs={'basket_thread_id': first_basket_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - ')
    assert response.context['basket_thread'] == first_basket_thread
    assert isinstance(response.context['form'], ThreadUpdateBasketForm)


def test_update_thread_basket_unauthenticated_redirects(client, first_basket_thread):
    # Act
    response = client.get(reverse('threads:update_thread_basket',
                                  kwargs={'basket_thread_id': first_basket_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_update_thread_basket_post_success(logged_in_client, first_basket_thread, basket):
    # Arrange
    client, user = logged_in_client
    data = {
        'quantity': 5.5,
    }

    # Act
    response = client.post(reverse('threads:update_thread_basket',
                           kwargs={'basket_thread_id': first_basket_thread.id}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:basket') in response.url
    assert BasketThread.objects.filter(
        basket=basket,
        thread=first_basket_thread.thread,
        quantity=5.5
    ).exists()


def test_update_thread_basket_user_cannot_update_another_users_project(logged_in_client, another_basket_thread):
    # Arrange
    client, user = logged_in_client
    data = {
        'quantity': 6.5,
    }

    # Act
    response = client.post(reverse('threads:update_thread_basket',
                           kwargs={'basket_thread_id': another_basket_thread.id}), data)

    # Assert
    assert response.status_code == 404


def test_update_thread_basket_invalid_basket_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_basket',
                                  kwargs={'basket_thread_id': 123}))

    # Assert
    assert response.status_code == 404


def test_delete_thread_basket_post_success(logged_in_client, first_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_basket',
                                   kwargs={'basket_thread_id': first_basket_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:basket') in response.url
    assert not BasketThread.objects.filter(id=first_basket_thread.id).exists()


def test_delete_thread_basket_user_cannot_delete_another_users_project(logged_in_client, another_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_basket',
                           kwargs={'basket_thread_id': another_basket_thread.id}))

    # Assert
    assert response.status_code == 404


def test_delete_thread_basket_method_get_no_delete(logged_in_client, first_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:delete_thread_basket',
                                  kwargs={'basket_thread_id': first_basket_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:basket') in response.url
    assert BasketThread.objects.filter(id=first_basket_thread.id).exists()


def test_delete_thread_basket_unauthenticated_redirects(client, first_basket_thread):
    # Act
    response = client.get(reverse('threads:delete_thread_basket',
                                  kwargs={'basket_thread_id': first_basket_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_delete_thread_basket_invalid_basket_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_basket',
                                   kwargs={'basket_thread_id': 123}))

    # Assert
    assert response.status_code == 404
