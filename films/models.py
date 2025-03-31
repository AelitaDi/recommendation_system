from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}


class Genre(models.Model):
    """
    Модель жанра.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Producer(models.Model):
    """
    Модель режиссера.
    """
    name = models.CharField(max_length=100, verbose_name='Режиссер')
    bio = models.TextField(**NULLABLE, verbose_name='Биография')

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'

    def __str__(self):
        return self.name


class Actor(models.Model):
    """
    Модель актера.
    """
    name = models.CharField(max_length=100, verbose_name='Актер')
    bio = models.TextField(**NULLABLE, verbose_name='Биография')

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

    def __str__(self):
        return self.name


class Film(models.Model):
    """
    Модель фильма.
    """
    title = models.CharField(max_length=150, verbose_name='Название', help_text='Введите название фильма')
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE, related_name="films", verbose_name='Режиссер')
    actors = models.ManyToManyField('Actor', related_name="films", verbose_name='В фильме снимались')
    genres = models.ManyToManyField('Genre', related_name="films", verbose_name='Жанр')
    release_year = models.IntegerField(validators=[MaxValueValidator(2025), MinValueValidator(1895)],
                                       verbose_name='Год выхода фильма')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    poster = models.ImageField(upload_to='films/posters/', **NULLABLE, verbose_name='Постер',
                               help_text='Загрузите постер')
    publish_date = models.DateField(auto_now_add=True)

    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Рейтинг фильма'
    )

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title
