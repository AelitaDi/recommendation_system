from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    UserCreateAPIView,
    UserUpdateAPIView,
    UserRetrieveAPIView,
    UserListAPIView,
    UserDestroyAPIView,
    StatisticsAPIView,
    RecommendationAPIView,
    InteractionViewSet,
)
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register("interactions", InteractionViewSet)

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("user_update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user_delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("user_list/", UserListAPIView.as_view(), name="users_list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("recommendations/", RecommendationAPIView.as_view(), name="recommendations"),
    path("statistics/", StatisticsAPIView.as_view(), name="statistics"),
]

urlpatterns += router.urls
