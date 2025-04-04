from django.urls import path

from films.apps import FilmsConfig
from films.views import FilmListView, FilmDetailView, GenreListView, GenreDetailView, GenreCreateView, GenreUpdateView, \
    GenreDeleteView, ProducerListView, ProducerDetailView, ProducerCreateView, ProducerUpdateView, ProducerDeleteView, \
    HomeView, FilmCreateView, FilmUpdateView, FilmDeleteView, ActorListView, ActorDetailView, ActorCreateView, \
    ActorUpdateView, ActorDeleteView

app_name = FilmsConfig.name

urlpatterns = [

    # Genres CRUD
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre_detail'),
    path('genres/new/', GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/edit/', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre_delete'),

    # Films CRUD
    path('films/', FilmListView.as_view(), name='film_list'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film_detail'),
    path('films/create/', FilmCreateView.as_view(), name='film_create'),
    path('films/<int:pk>/update/', FilmUpdateView.as_view(), name='film_update'),
    path('films/<int:pk>/delete/', FilmDeleteView.as_view(), name='film_delete'),

    # Producers CRUD
    path('producers/', ProducerListView.as_view(), name='producers'),
    path('producers/<int:pk>/', ProducerDetailView.as_view(), name='producer_detail'),
    path('producers/create/', ProducerCreateView.as_view(), name='producer_create'),
    path('producers/<int:pk>/update/', ProducerUpdateView.as_view(), name='producer_update'),
    path('producers/<int:pk>/delete/', ProducerDeleteView.as_view(), name='producer_delete'),

    # Actors CRUD
    path('actors/', ActorListView.as_view(), name='actor_list'),
    path('actors/<int:pk>/', ActorDetailView.as_view(), name='actor_detail'),
    path('actors/create/', ActorCreateView.as_view(), name='actor_create'),
    path('actors/<int:pk>/update/', ActorUpdateView.as_view(), name='actor_update'),
    path('actors/<int:pk>/delete/', ActorDeleteView.as_view(), name='actor_delete'),

    # Home
    path('', HomeView.as_view(), name='home'),

    # Statistics
    # path('statistics/', StatisticsView.as_view(), name='statistics')
]
