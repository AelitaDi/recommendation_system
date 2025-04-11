from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

import films.models
import users.models

NULLABLE = {"blank": True, "null": True}


class Interaction(models.Model):
    """
    Модель взаимосвязи.
    """

    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE)
    film = models.ForeignKey(films.models.Film, on_delete=models.CASCADE)

    rating = models.IntegerField(
        **NULLABLE,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Взаимосвязь"
        verbose_name_plural = "Взаимосвязи"
        unique_together = (("user", "film"),)
        indexes = [models.Index(fields=["user", "film"])]

    def save(self, *args, **kwargs):
        """
        Метод обновления среднего рейтинга фильма при добавлении (изменении) взаимосвязи.
        """
        if self.pk:
            instance = Interaction.objects.get(pk=self.pk)
            if instance.user != self.user:
                raise PermissionDenied("Вы не можете изменить чужую оценку фильма.")
        super().save(*args, **kwargs)
        self.film.average_rating = (
            Interaction.objects.filter(film=self.film).aggregate(Avg("rating"))[
                "rating__avg"
            ]
            or 0.0
        )
        print(self.film.average_rating)

        self.film.save()

    def __str__(self):
        return f"{self.user} {self.film} {self.rating}"
