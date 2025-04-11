import os

import django

from recommendations.services import graph_builder, create_recommendation
from users.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import networkx as nx
from interactions.models import Interaction


class PageRank:
    @staticmethod
    def recommendations(user_id, top_n=10):
        """
        Получение рекомендаций (top_n фильмов) на основе алгоритма PageRank.
        """
        G = graph_builder()

        if not G.nodes:
            return []

        pr = nx.pagerank(G, weight="weight")

        if not any(node.startswith("film_") for node in pr):
            return []

        user_films = set(
            Interaction.objects.filter(user_id=user_id).values_list(
                "film_id", flat=True
            )
        )

        ranked_films = {
            int(node.split("_")[1]): rank
            for node, rank in pr.items()
            if node.startswith("film_") and int(node.split("_")[1]) not in user_films
        }

        if not ranked_films:
            return []

        sorted_films = sorted(
            ranked_films.items(), key=lambda items: items[1], reverse=True
        )[:top_n]
        top_n_films = list(film_id for film_id, rank in sorted_films)

        # Создание рекомендации
        user = User.objects.get(id=user_id)
        recommendation = create_recommendation(user, "pagerank", top_n_films)

        return list(recommendation.films.all())
