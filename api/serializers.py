from rest_framework.serializers import ModelSerializer

from interactions.models import Interaction
from users.models import User


class InteractionSerializer(ModelSerializer):
    """
    Сериализатор для взаимодействий.
    """

    class Meta:
        model = Interaction
        fields = "__all__"


class UserSelfSerializer(ModelSerializer):
    """
    Сериализатор для создания, редактирования и просмотра собственного профиля.
    """

    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """
    Сериализатор для просмотра общей информации о пользователях.
    """

    interactions = InteractionSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("email", "is_active", "is_staff", "id", "interactions", "preferred_genres")
