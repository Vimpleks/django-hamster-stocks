from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя.
    """
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователя.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class ProfileForm(UserChangeForm):
    """
    Форма для просмотра или изменения информации о пользователе.
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
