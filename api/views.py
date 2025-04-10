from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsSelf, IsStaffUser
from api.serializers import UserSelfSerializer, UserSerializer, InteractionSerializer
from interactions.models import Interaction
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
