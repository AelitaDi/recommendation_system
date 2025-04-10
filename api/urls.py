from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, UserListAPIView, UserDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),

    path("user_update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user_delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("user_list/", UserListAPIView.as_view(), name="users_list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),

    # path('recommendations/pagerank/', get_pagerank_recommendations, name='get-my-pr-recommendations'),
    # path('recommendations/knn/', get_knn_recommendations, name='get-my-knn-recommendations'),
    # path('statistics/', get_statistics_api, name='statistics')
]
