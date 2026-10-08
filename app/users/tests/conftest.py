import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='test-password-123',
        first_name='Иван',
        last_name='Петров',
    )


@pytest.fixture
def logged_in_client(client, user):
    client.login(username='testuser', password='test-password-123')
    return client, user
