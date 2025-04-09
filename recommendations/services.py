import os
import django

from recommendations.algorithms.pagerank import PageRank

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


import networkx as nx
import matplotlib.pyplot as plt

from films.models import Film
from interactions.models import Interaction
from users.models import User


def graph_builder():
    """
    Построение ненаправленного графа.
    """
    G = nx.Graph()

    for user in User.objects.all():
        G.add_node(f'user_{user.id}', type='user')

    for film in Film.objects.all():
        G.add_node(f'film_{film.id}', type='film')

    for interaction in Interaction.objects.select_related('user', 'film'):
        user_node = f'user_{interaction.user.id}'
        film_node = f'film_{interaction.film.id}'
        weight = interaction.rating if interaction.rating else 1.0
        G.add_edge(user_node, film_node, weight=weight)

    return G


def digraph_builder():
    """
    Построение направленного графа.
    """
    DG = nx.DiGraph()

    for user in User.objects.all():
        DG.add_node(f'user_{user.id}', type='user')

    for film in Film.objects.all():
        DG.add_node(f'film_{film.id}', type='film')

    for interaction in Interaction.objects.select_related('user', 'film'):
        user_node = f'user_{interaction.user.id}'
        film_node = f'film_{interaction.film.id}'
        weight = interaction.rating if interaction.rating else 1.0
        DG.add_edge(user_node, film_node, weight=weight)

    return DG


def get_graph_visualization(G):
    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == '__main__':
    g = graph_builder()
    # pos = nx.circular_layout(g)
    # get_graph_visualization(g)
    print(PageRank.recommendations(4, g, 5))
