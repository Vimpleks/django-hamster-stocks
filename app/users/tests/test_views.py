from threads.models import Stock, Basket
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User


def test_login_get_returns_form(client):
    # Act
    response = client.get(reverse('users:login'))

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserLoginForm)


def test_login_success_redirects(client, user):
    # Arrange
    data = {
        'username': user.username,
        'password': 'test-password-123',
    }

    # Act
    response = client.post(reverse('users:login'), data=data)

    # Assert
    assert response.status_code == 302
    assert response.url == reverse('threads:index')
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user == user


def test_login_invalid_credentials_stays_on_page(client, user):
    # Arrange
    data = {
        "username": user.username,
        "password": "wrongpassword",
    }

    # Act
    response = client.post(reverse('users:login'), data=data)

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert not response.wsgi_request.user.is_authenticated
    assert not response.context['form'].is_valid()


def test_login_nonexistent_user_stays_on_page(client, db):
    # Arrange
    data = {
        "username": "nonexistent",
        "password": "anypassword",
    }

    # Act
    response = client.post(reverse('users:login'), data=data)

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert not response.wsgi_request.user.is_authenticated


def test_registration_get_returns_form(client):
    # Act
    response = client.get(reverse('users:registration'))

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserRegistrationForm)


def test_registration_success_creates_user_and_objects(client, db):
    # Arrange
    data = {
        'username': 'user1',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'email': 'test@mail.ru'
    }

    # Act
    response = client.post(reverse('users:registration'), data=data)

    # Assert
    assert response.status_code == 302
    assert response.url == reverse('threads:index')
    user = User.objects.filter(username="user1").first()
    assert user is not None
    assert Stock.objects.filter(owner=user).exists()
    assert Basket.objects.filter(owner=user).exists()
    assert response.wsgi_request.user == user
    assert response.wsgi_request.user.is_authenticated


def test_registration_duplicate_username_fails(client, user):
    # Arrange
    data = {
        'username': 'testuser',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'email': 'test1@mail.ru'
    }

    # Act
    response = client.post(reverse('users:registration'), data=data)

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert not response.context['form'].is_valid()


def test_profile_requires_login(client):
    # Act
    response = client.get(reverse('users:profile'))

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_profile_get_returns_form_with_user_data(logged_in_client, user):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('users:profile'))

    # Assert
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].initial['first_name'] == user.first_name
    assert response.context['form'].initial['last_name'] == user.last_name
    assert response.context['form'].initial['email'] == user.email


def test_profile_update_successfully_saves_changes(logged_in_client, user):
    # Arrange
    client, user = logged_in_client
    data = {
        'username': user.username,
        'first_name': 'NewFirstName',
        'last_name': 'NewLastName',
        'email': 'new@example.com',
    }

    # Act
    response = client.post(reverse('users:profile'), data=data)

    # Assert
    assert response.status_code == 302
    assert response.url == reverse('users:profile')
    assert User.objects.filter(
        username=user.username,
        first_name='NewFirstName',
        last_name='NewLastName',
        email='new@example.com'
    ).exists()


def test_logout_unauthenticated_redirects(client):
    # Act
    response = client.post(reverse('users:logout'))

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_logout_success_get_logs_out_and_redirects(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('users:logout'))

    # Assert
    assert response.status_code == 302
    assert response.url == reverse('threads:index')
    assert not client.get('/').wsgi_request.user.is_authenticated


def test_logout_success_post_logs_out_and_redirects(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('users:logout'))

    # Assert
    assert response.status_code == 302
    assert response.url == reverse('threads:index')
    assert not client.get('/').wsgi_request.user.is_authenticated
