from django.contrib import admin

from recommendations.models import Recommendation


@admin.register(Recommendation)
class InteractionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
    )
    list_filter = ("user",)
    search_fields = ("user__username",)
    ordering = ("-created_at",)
