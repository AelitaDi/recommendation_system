from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from films.forms import StyleFormMixin
from films.models import Genre
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Предпочитаемые жанры'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'preferred_genres')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class UserUpdateForm(StyleFormMixin, UserCreationForm):
    """
    Форма редактирования данных пользователя.
    """
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Предпочитаемые жанры'
    )

    class Meta:
        model = User
        fields = ('phone_number', 'avatar', 'city', 'preferred_genres',)
