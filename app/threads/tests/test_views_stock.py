from django.urls import reverse

from threads.forms import ThreadQuantityForm, ThreadUpdateStockForm
from threads.models import StockThread


def test_stock_authenticated_user(logged_in_client, some_stock_threads):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:stock'))

    # Assert
    assert response.status_code == 200
    assert response.context['title'] == 'Запасы хомяка - Твои запасы'
    assert list(response.context['stock_threads']) == list(some_stock_threads)
    assert 'total_color' in response.context
    assert 'total_quantity' in response.context
    assert response.context['filter_value'] is None


def test_stock_unauthenticated_redirects(client):
    # Act
    response = client.get(reverse('threads:stock'), follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_stock_filters_by_article(logged_in_client, some_stock_threads):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:stock'), {'article': 'B5200'})

    # Assert
    assert response.status_code == 200
    assert response.context['stock_threads'].count() == 1
    assert response.context['stock_threads'].first().thread.article == 'B5200'
    assert response.context['filter_value'] == 'B5200'


def test_add_thread_stock_authenticated_user(logged_in_client, manufacturer, first_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_stock',
                          kwargs={'manufacturer_slug': manufacturer.slug}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - Нитки')
    assert response.context['manufacturer'] == manufacturer
    assert list(response.context['threads']) == [first_thread]
    assert response.context['filter_value'] is None
    assert isinstance(response.context['form'], ThreadQuantityForm)


def test_add_thread_stock_unauthenticated_redirects(client, manufacturer):
    # Act
    response = client.get(reverse('threads:add_thread_stock',
                          kwargs={'manufacturer_slug': manufacturer.slug}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_add_thread_stock_filters_by_article(logged_in_client, manufacturer, first_thread, second_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_stock',
                          kwargs={'manufacturer_slug': manufacturer.slug}),
                          {'article': 'B5200'})

    # Assert
    assert response.status_code == 200
    assert response.context['threads'].count() == 1
    assert response.context['threads'].first().article == 'B5200'
    assert response.context['filter_value'] == 'B5200'


def test_add_thread_stock_post_success(logged_in_client, manufacturer, second_thread, stock):
    # Arrange
    client, user = logged_in_client
    data = {
        'thread': second_thread.id,
        'quantity': 5.5,
    }

    # Act
    response = client.post(reverse('threads:add_thread_stock',
                           kwargs={'manufacturer_slug': manufacturer.slug}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:stock') in response.url
    assert StockThread.objects.filter(
        stock=stock,
        thread=second_thread,
        quantity=5.5
    ).exists()


def test_add_thread_stock_invalid_slug_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_stock',
                                  kwargs={'manufacturer_slug': 'nonexistent-slug'}))

    # Assert
    assert response.status_code == 404


def test_update_thread_stock_authenticated_user(logged_in_client, first_stock_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_stock',
                                  kwargs={'stock_thread_id': first_stock_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - ')
    assert response.context['stock_thread'] == first_stock_thread
    assert isinstance(response.context['form'], ThreadUpdateStockForm)


def test_update_thread_stock_unauthenticated_redirects(client, first_stock_thread):
    # Act
    response = client.get(reverse('threads:update_thread_stock',
                                  kwargs={'stock_thread_id': first_stock_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_update_thread_stock_post_success(logged_in_client, first_stock_thread, stock):
    # Arrange
    client, user = logged_in_client
    data = {
        'quantity': 5.5,
    }

    # Act
    response = client.post(reverse('threads:update_thread_stock',
                           kwargs={'stock_thread_id': first_stock_thread.id}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:stock') in response.url
    assert StockThread.objects.filter(
        stock=stock,
        thread=first_stock_thread.thread,
        quantity=5.5
    ).exists()


def test_update_thread_stock_user_cannot_update_another_users_stock(logged_in_client, another_stock_thread):
    # Arrange
    client, user = logged_in_client
    data = {
        'quantity': 6.5,
    }

    # Act
    response = client.post(reverse('threads:update_thread_stock',
                           kwargs={'stock_thread_id': another_stock_thread.id}), data)

    # Assert
    assert response.status_code == 404


def test_update_thread_stock_invalid_stock_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_stock',
                                  kwargs={'stock_thread_id': 123}))

    # Assert
    assert response.status_code == 404


def test_delete_thread_stock_post_success(logged_in_client, first_stock_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_stock',
                                   kwargs={'stock_thread_id': first_stock_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:stock') in response.url
    assert not StockThread.objects.filter(id=first_stock_thread.id).exists()


def test_delete_thread_stock_user_cannot_delete_another_users_stock(logged_in_client, another_stock_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_stock',
                           kwargs={'stock_thread_id': another_stock_thread.id}))

    # Assert
    assert response.status_code == 404


def test_delete_thread_stock_method_get_no_delete(logged_in_client, first_stock_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:delete_thread_stock',
                                  kwargs={'stock_thread_id': first_stock_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:stock') in response.url
    assert StockThread.objects.filter(id=first_stock_thread.id).exists()


def test_delete_thread_stock_unauthenticated_redirects(client, first_stock_thread):
    # Act
    response = client.get(reverse('threads:delete_thread_stock',
                                  kwargs={'stock_thread_id': first_stock_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_delete_thread_stock_invalid_stock_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_stock',
                                   kwargs={'stock_thread_id': 123}))

    # Assert
    assert response.status_code == 404
