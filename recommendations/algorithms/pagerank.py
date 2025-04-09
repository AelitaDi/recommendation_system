import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import networkx as nx
from django.core.cache import cache

from config.settings import CACHE_ENABLED, CACHE_TIMEOUT
from films.models import Film
from interactions.models import Interaction


class PageRank:
    @staticmethod
    def recommendations(user_id, G, top_n=10):
        """
        Получение рекомендаций (top_n фильмов) на основе алгоритма PageRank.
        """
        cache_key = 'pr_rec'

        if not G.nodes:
            return []

        if CACHE_ENABLED:
            pr = cache.get(cache_key)
            if pr is None:
                pr = nx.pagerank(G, weight='weight')
                cache.set(cache_key, pr, timeout=CACHE_TIMEOUT)
        else:
            pr = nx.pagerank(G, weight='weight')

        if not any(node.startswith('film_') for node in pr):
            return []

        user_films = set(Interaction.objects.filter(user_id=user_id).values_list('film_id', flat=True))

        ranked_films = {
            int(node.split('_')[1]): rank
            for node, rank in pr.items()
            if node.startswith('film_') and int(node.split('_')[1]) not in user_films
        }

        if not ranked_films:
            return []

        sorted_films = sorted(ranked_films.items(), key=lambda items: items[1], reverse=True)[:top_n]
        # top_n_films = [{Film.objects.get(id=film_id): rank} for film_id, rank in sorted_films]
        top_n_films = [Film.objects.get(id=film_id) for film_id, rank in sorted_films]

        return top_n_films
