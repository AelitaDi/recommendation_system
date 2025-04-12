from django.contrib import admin

from films.models import Film, Genre, Actor, Producer


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_filter = ("producer", "actors", "release_year", "genres")
    search_fields = ("title",)
    ordering = (
        "-release_year",
        "title",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)
