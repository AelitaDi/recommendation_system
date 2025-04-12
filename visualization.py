import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from recommendations.services import (
    get_graph_visualization,
    digraph_builder,
)

if __name__ == "__main__":
    G = digraph_builder()
    get_graph_visualization(G)
