from rest_framework.serializers import ModelSerializer

from films.models import Film, Producer, Actor, Genre
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


class GenreSerializer(ModelSerializer):
    """
    Сериализатор для жанра.
    """

    class Meta:
        model = Genre
        fields = ["id", "name"]


class ProducerSerializer(ModelSerializer):
    """
    Сериализатор для режиссера.
    """

    class Meta:
        model = Producer
        fields = "__all__"


class ActorSerializer(ModelSerializer):
    """
    Сериализатор для актера.
    """

    class Meta:
        model = Actor
        fields = "__all__"


class FilmSerializer(ModelSerializer):
    """
    Сериализатор для фильмов.
    """

    class Meta:
        model = Film
        fields = ["id", "title", "release_year", "average_rating"]


class FilmDetailSerializer(ModelSerializer):
    """
    Сериализатор для фильма, подробный.
    """

    producer = ProducerSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "release_year",
            "average_rating",
            "genres",
            "actors",
            "producer",
            "description",
        ]


class UserSerializer(ModelSerializer):
    """
    Сериализатор для просмотра общей информации о пользователях.
    """

    interactions = InteractionSerializer(read_only=True, many=True)
    preferred_genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "email",
            "is_active",
            "is_staff",
            "id",
            "interactions",
            "preferred_genres",
        )
