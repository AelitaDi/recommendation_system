from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mail_service.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    """
    Форма редактирования данных пользователя.
    """
    password = None

    class Meta:
        model = User
        fields = ('phone_number', 'avatar', 'country')
