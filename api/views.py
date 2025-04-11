from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsSelf, IsStaffUser
from api.serializers import (
    UserSelfSerializer,
    UserSerializer,
    InteractionSerializer,
    FilmSerializer,
    FilmDetailSerializer,
)
from films.models import Film
from interactions.models import Interaction
from recommendations.algorithms.knn import KNN
from recommendations.algorithms.pagerank import PageRank
from recommendations.services import get_statistics
from users.models import User


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSelfSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated, IsSelf]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated, IsSelf]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Interaction.objects.all()
        return Interaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FilmViewSet(ModelViewSet):

    def get_queryset(self):
        return Film.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FilmDetailSerializer
        return FilmSerializer


class StatisticsAPIView(APIView):
    """
    Отображение статистики сервиса.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        statistics_data = get_statistics()
        serialized_data = {
            "top_rated_films": FilmSerializer(
                statistics_data["top_rated_films"], many=True
            ).data,
            "top_active_users": UserSerializer(
                statistics_data["top_active_users"], many=True
            ).data,
        }
        statistics_data.update(serialized_data)

        return Response(statistics_data)


class RecommendationAPIView(APIView):
    """
    Получение рекомендаций сервиса.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pr_rec = PageRank.recommendations(request.user.id, 10)
        knn_rec = KNN.recommendations(request.user.id, 10)
        serialized_data = {
            "pr_rec": FilmSerializer(pr_rec, many=True).data,
            "knn_rec": FilmSerializer(knn_rec, many=True).data,
        }

        return Response(serialized_data)
