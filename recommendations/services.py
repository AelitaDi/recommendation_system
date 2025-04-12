import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db.models import Count, Q
from django.utils import timezone

import networkx as nx
import matplotlib.pyplot as plt

from recommendations.models import Recommendation
from films.models import Film
from interactions.models import Interaction
from users.models import User


def graph_builder():
    """
    Построение ненаправленного графа.
    """
    G = nx.Graph()

    for user in User.objects.all():
        G.add_node(f"user_{user.id}", type="user")

    for film in Film.objects.all():
        G.add_node(f"film_{film.id}", type="film")

    for interaction in Interaction.objects.select_related("user", "film"):
        user_node = f"user_{interaction.user.id}"
        film_node = f"film_{interaction.film.id}"
        weight = interaction.rating if interaction.rating else 1.0
        G.add_edge(user_node, film_node, weight=weight)

    return G


def digraph_builder():
    """
    Построение направленного графа.
    """
    DG = nx.DiGraph()

    for user in User.objects.all():
        DG.add_node(f"user_{user.id}", type="user")

    for film in Film.objects.all():
        DG.add_node(f"film_{film.id}", type="film")

    for interaction in Interaction.objects.select_related("user", "film"):
        user_node = f"user_{interaction.user.id}"
        film_node = f"film_{interaction.film.id}"
        weight = interaction.rating if interaction.rating else 1.0
        DG.add_edge(user_node, film_node, weight=weight)

    return DG


def get_graph_visualization(G):
    """
    Визуализация графа.
    """

    # Вычисляем PageRank
    pagerank = nx.pagerank(G)

    # Нормализуем значения PageRank для размеров узлов
    node_sizes = [v * 100000 for v in pagerank.values()]

    # Рисуем граф
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)

    # Рисуем узлы с разными размерами
    values = [pagerank[n] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=values)

    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10)

    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    for node, (x, y) in pos.items():
        plt.text(x, y + 0.1, f"{pagerank[node]:.3f}",
                 fontsize=9, ha='center', color='red')

    plt.title("Граф с узлами, размер которых зависит от PageRank")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def create_recommendation(user, method, films_list):
    """
    Запись результатов алгоритмов в БД (создание экземпляра рекомендации).
    """
    recommendation = Recommendation.objects.create(user=user, method=method)
    recommendation.films.add(*Film.objects.filter(id__in=films_list))
    recommendation.save()
    return recommendation


def get_statistics():

    films_count = Film.objects.all().count()

    users_count = User.objects.all().count()

    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    new_films_week_count = Film.objects.filter(publish_date__gte=one_week_ago).count()

    top_rated_films = Film.objects.annotate(
        rating_count=Count("interaction__rating")
    ).order_by("-average_rating", "-rating_count")[:5]

    top_active_users = User.objects.annotate(
        interaction_count=Count(
            "interaction", filter=Q(interaction__timestamp__gte=one_week_ago)
        )
    ).order_by("-interaction_count")[:5]

    statistics_data = {
        "films_count": films_count,
        "users_count": users_count,
        "new_films_week_count": new_films_week_count,
        "top_rated_films": top_rated_films,
        "top_active_users": top_active_users,
    }

    return statistics_data
