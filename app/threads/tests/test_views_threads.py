from django.urls import reverse


def test_manufacturer_view_returns_200(client, manufacturer):
    # Act
    response = client.get(reverse('threads:manufacturers'))

    # Assert
    assert response.status_code == 200
    assert response.context['title'] == 'Запасы хомяка - Производители'
    assert list(response.context['manufacturers']) == [manufacturer]
    assert response.context['source'] == 'index'
    assert response.context['project'] is None


def test_manufacturer_get_source_param(client, db):
    # Act
    response = client.get(reverse('threads:manufacturers'), {'source': 'stock'})

    # Assert
    assert response.status_code == 200
    assert response.context['source'] == 'stock'


def test_manufacturer_get_project_id_param(client, db):
    # Act
    response = client.get(reverse('threads:manufacturers'), {'project_id': 123})

    # Assert
    assert response.status_code == 200
    assert response.context['project'] == '123'


def test_manufacturer_detail_returns_200(client, manufacturer, first_thread):
    # Act
    response = client.get(reverse('threads:manufacturer_detail',
                                  kwargs={'manufacturer_slug': manufacturer.slug}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - Нитки')
    assert response.context['manufacturer'] == manufacturer
    assert list(response.context['threads']) == [first_thread]
    assert response.context['filter_value'] is None


def test_manufacturer_detail_filters_by_article(client, manufacturer, first_thread, second_thread):
    # Act
    response = client.get(reverse('threads:manufacturer_detail',
                                  kwargs={'manufacturer_slug': manufacturer.slug}),
                          {'article': 'B5200'})

    # Assert
    assert response.status_code == 200
    assert response.context['threads'].count() == 1
    assert response.context['threads'].first().article == 'B5200'
    assert response.context['filter_value'] == 'B5200'


def test_manufacturer_detail_invalid_slug_returns_404(client, db):
    # Act
    response = client.get(reverse('threads:manufacturer_detail',
                                  kwargs={'manufacturer_slug': 'nonexistent-slug'}))

    # Assert
    assert response.status_code == 404


def test_thread_detail_authenticated_user(logged_in_client, first_thread, some_stock_threads, some_basket_threads,
                                          first_project_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:thread_detail',
                                  kwargs={'thread_id': first_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - ')
    assert response.context['thread'] == first_thread
    assert response.context['stock_count'] == 1.5
    assert response.context['basket_count'] == 1.5
    assert list(response.context['project_threads']) == [first_project_thread]


def test_thread_detail_unauthenticated_redirects(client, first_thread):
    # Act
    response = client.get(reverse('threads:thread_detail',
                                  kwargs={'thread_id': first_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_thread_detail_invalid_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:thread_detail',
                                  kwargs={'thread_id': 123}))

    # Assert
    assert response.status_code == 404


def test_thread_detail_stock_count_zero_if_not_in_stock(logged_in_client, second_thread, first_stock_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:thread_detail',
                                  kwargs={'thread_id': second_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['thread'] == second_thread
    assert response.context['stock_count'] == 0


def test_thread_detail_basket_count_zero_if_not_in_basket(logged_in_client, second_thread, first_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:thread_detail',
                                  kwargs={'thread_id': second_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['thread'] == second_thread
    assert response.context['basket_count'] == 0
