from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {
    'blank': True,
    'null': True
}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    city = models.CharField(max_length=150, verbose_name="Город", help_text="Введите город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        help_text="Загрузите ваш аватар",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email
