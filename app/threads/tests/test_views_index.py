from django.urls import reverse


def test_index_returns_200(client):
    # Act
    response = client.get(reverse('threads:index'))

    # Assert
    assert response.status_code == 200


def test_index_title_available_in_template(client):
    # Act
    response = client.get(reverse('threads:index'))

    # Assert
    assert 'Запасы хомяка' in response.content.decode('utf-8')
