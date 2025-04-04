from django.urls import path

from recommendations.apps import RecommendationsConfig

app_name = RecommendationsConfig.name

urlpatterns = [
    # Recommendations
    # path('recommendations/', RecommendationView.as_view(), name='recommendations'),

    # Statistics
    # path('statistics/', StatisticsView.as_view(), name='statistics')
]
