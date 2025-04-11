from django.db import models

from films.models import Film
from users.models import User


class Recommendation(models.Model):
    """
    Модель рекомендации.
    """

    METHOD_CHOICES = [
        ("knn", "Алгоритм ближайших соседей"),
        ("pagerank", "Алгоритм PageRank"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recommendations"
    )
    films = models.ManyToManyField(
        Film, related_name="recommendations", verbose_name="Ваши рекомендации"
    )
    method = models.CharField(
        max_length=9, choices=METHOD_CHOICES, verbose_name="Алгоритм"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"

    def __str__(self):
        return f"Рекомендация для {self.user.email} по методу {self.method} от {self.created_at}"
