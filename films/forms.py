from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from films.models import Film, Genre, Producer, Actor


class StyleFormMixin:
    """
    Миксин для настройки стилей форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class FilmForm(StyleFormMixin, forms.ModelForm):
    """
    Форма фильма.
    """

    producer = forms.ModelChoiceField(queryset=Producer.objects.all(), label="Режиссер")
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple, label="Жанры"
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Актеры",
    )

    class Meta:
        model = Film
        fields = (
            "title",
            "producer",
            "actors",
            "poster",
            "genres",
            "release_year",
            "description",
        )

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"placeholder": "Введите название фильма"}
        )

        self.fields["description"].widget.attrs.update(
            {"placeholder": "Введите краткое описание фильма"}
        )

        self.fields["producer"].widget.attrs.update(
            {"placeholder": "Выберите режиссера"}
        )

        self.fields["actors"].widget.attrs.update({"placeholder": "Выберите актеров"})

        self.fields["genres"].widget.attrs.update(
            {"placeholder": "Выберите подходящие жанры"}
        )

        self.fields["release_year"].widget.attrs.update(
            {"placeholder": "Введите год выхода фильма"}
        )

        self.fields["poster"].widget.attrs.update(
            {"placeholder": "Загрузите постер к фильму"}
        )

    def clean_image(self):
        imagesize = self.cleaned_data.get("poster").size
        if imagesize > 5242880:
            raise ValidationError("Вы не можете загрузить файл больше 5Mb")
        return self.cleaned_data.get("poster")


class GenreForm(StyleFormMixin, forms.ModelForm):
    """
    Форма жанра.
    """

    class Meta:
        model = Genre
        fields = [
            "name",
        ]


class ProducerForm(StyleFormMixin, forms.ModelForm):
    """
    Форма режиссера.
    """

    class Meta:
        model = Producer
        fields = ["name", "bio"]


class ActorForm(StyleFormMixin, forms.ModelForm):
    """
    Форма актера.
    """

    class Meta:
        model = Actor
        fields = ["name", "bio"]
