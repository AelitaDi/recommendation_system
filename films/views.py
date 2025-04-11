from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
)

from config.settings import CACHE_ENABLED
from films.forms import FilmForm, GenreForm, ProducerForm, ActorForm
from films.models import Film, Genre, Producer, Actor
from interactions.forms import InteractionForm
from interactions.models import Interaction
from recommendations.algorithms.knn import KNN
from recommendations.algorithms.pagerank import PageRank
from recommendations.services import get_statistics


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Миксин проверяет наличие у пользователя прав is_staff.
    """

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас недостаточно прав для этого действия.")


class HomeView(TemplateView):
    """
    Home view.
    """

    template_name = "films/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RecommendationView(LoginRequiredMixin, TemplateView):
    """
    Контроллер для отображения рекомендаций.
    """

    template_name = "films/recommendations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if not CACHE_ENABLED:
            recs = {
                "pr_rec": PageRank.recommendations(user_id, 10),
                "knn_rec": KNN.recommendations(user_id, 10),
            }
        else:
            key = "recs"
            recs = cache.get(key)
            if not recs:
                recs = {
                    "pr_rec": PageRank.recommendations(user_id, 10),
                    "knn_rec": KNN.recommendations(user_id, 10),
                }
                cache.set("recs", recs, timeout=300)
        context.update(recs)
        return context


class StatisticsView(TemplateView):
    """
    Контроллер для отображения статистика сервиса.
    """

    pass
    template_name = "films/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics_data = get_statistics()
        context.update(statistics_data)

        return context


# Genre CRUD
class GenreListView(ListView):
    model = Genre
    paginate_by = 20


class GenreDetailView(DetailView):
    model = Genre


class GenreCreateView(StaffRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy("films:genre_list")


class GenreUpdateView(StaffRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy("films:genre_list")


class GenreDeleteView(StaffRequiredMixin, DeleteView):
    model = Genre
    success_url = reverse_lazy("films:genre_list")


# Producer CRUD
class ProducerListView(ListView):
    model = Producer
    paginate_by = 10


class ProducerDetailView(DetailView):
    model = Producer


class ProducerCreateView(StaffRequiredMixin, CreateView):
    model = Producer
    form_class = ProducerForm
    success_url = reverse_lazy("films:producer_list")


class ProducerUpdateView(StaffRequiredMixin, UpdateView):
    model = Producer
    form_class = ProducerForm
    success_url = reverse_lazy("films:producer_list")


class ProducerDeleteView(StaffRequiredMixin, DeleteView):
    model = Producer
    success_url = reverse_lazy("films:producer_list")


# Actor CRUD
class ActorListView(ListView):
    model = Actor
    paginate_by = 10


class ActorDetailView(DetailView):
    model = Actor


class ActorCreateView(StaffRequiredMixin, CreateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor_list")


class ActorUpdateView(StaffRequiredMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor_list")


class ActorDeleteView(StaffRequiredMixin, DeleteView):
    model = Actor
    success_url = reverse_lazy("films:actor_list")


# Film CRUD
class FilmListView(ListView):
    model = Film
    paginate_by = 10

    # def get_queryset(self):
    #     if not CACHE_ENABLED:
    #         return super().get_queryset()
    #     key = "products_list"
    #     products = cache.get(key)
    #     if products is not None:
    #         return products
    #     products = super().get_queryset()
    #     cache.set(key, products, 60 * 15)
    #     return products


@method_decorator(login_required, name="dispatch")
class FilmDetailView(LoginRequiredMixin, DetailView):
    model = Film

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        interaction = Interaction.objects.filter(
            user=self.request.user, film=film
        ).first()
        context["interaction_form"] = InteractionForm(instance=interaction)
        context["user_rating"] = interaction.rating if interaction else None
        return context

    def post(self, request, *args, **kwargs):
        film = self.get_object()
        interaction, created = Interaction.objects.get_or_create(
            user=request.user, film=film
        )
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            form.save()
        return redirect("films:film_detail", pk=film.pk)


class FilmCreateView(StaffRequiredMixin, CreateView):
    model = Film
    form_class = FilmForm
    success_url = reverse_lazy("films:film_list")


class FilmUpdateView(StaffRequiredMixin, UpdateView):
    model = Film
    form_class = FilmForm
    success_url = reverse_lazy("films:film_list")


class FilmDeleteView(StaffRequiredMixin, DeleteView):
    model = Film
    success_url = reverse_lazy("films:film_list")
