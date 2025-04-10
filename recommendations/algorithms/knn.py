import os
import django

from recommendations.services import create_recommendation

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import math

from films.models import Film
from interactions.models import Interaction
from users.models import User
from recommendations.models import Recommendation


class KNN:
    @staticmethod
    def recommendations(user_id, top_n=10):
        """
        Нахождение n ближайших соседей на основе общих интересов.
        """
        ranked_films = list(
            Interaction.objects.filter(user=user_id).exclude(rating=None).values_list('film_id', flat=True))
        # print(ranked_films)

        neighbours = list(
            Interaction.objects.filter(film_id__in=ranked_films, rating__isnull=False).distinct().exclude(
                user=user_id).values_list('user_id',
                                          flat=True))

        # Вычисление "расстояний" между пользователями
        nei_dist_list = []
        for nei in neighbours:
            total = 0
            for film in ranked_films:
                a = Interaction.objects.get(user=user_id, film=film).rating
                if Interaction.objects.filter(user=nei, film=film).exclude(rating=None).exists():
                    b = Interaction.objects.get(user=nei, film=film).rating
                    total += (a - b) ** 2
            distance = math.sqrt(total)
            nei_dist_list.append({'user': nei, 'distance': distance})

        # Сортировка пользователей по близости
        sorted_nei_list = sorted(nei_dist_list, key=lambda x: x['distance'])
        sorted_nei = list(nei['user'] for nei in sorted_nei_list)

        k = round(math.sqrt(len(User.objects.all())))
        top_films = Interaction.objects.filter(user_id__in=sorted_nei[:k], rating__gte=4).exclude(
            film_id__in=ranked_films).values_list('film_id', flat=True).distinct()

        # Получение списка фильмов
        rec_films = []
        for f in top_films:
            rec_films.append({'film_id': f, 'av_r': Film.objects.get(id=f).average_rating})

        sorted_top_n_rec_films = sorted(rec_films, key=lambda x: x['av_r'], reverse=True)[:top_n]
        film_id_list = list(x['film_id'] for x in sorted_top_n_rec_films)

        # Создание рекомендации
        user = User.objects.get(id=user_id)
        recommendation = create_recommendation(user, 'knn', film_id_list)

        return list(recommendation.films.all())


if __name__ == '__main__':
    print(KNN.recommendations(66, 5))
