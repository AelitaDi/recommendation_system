import networkx as nx

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from recommendations.services import (
    graph_builder,
    get_graph_visualization,
    # digraph_builder,
)

if __name__ == "__main__":
    g = graph_builder()
    # g = digraph_builder()
    pos = nx.circular_layout(g)
    get_graph_visualization(g)
