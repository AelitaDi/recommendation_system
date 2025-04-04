from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class RecommendationView(LoginRequiredMixin, TemplateView):
    """
    Контроллер для отображения рекомендаций.
    """
    # template_name = 'books/recommendations.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_id = self.request.user.id
    #     context["pagerank_recommendations"] = get_pagerank_recommendations_service(user_id)
    #     context['collaborative_recommendations'] = get_collaborative_recommendations_service(user_id)
    #     context['knn_recommendations'] = get_knn_recommendations_service(user_id)
    #
    #     return context
    pass
