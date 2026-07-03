from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "venue",
        "start_date",
        "end_date",
        "status",
        "registration_fee",
    )

    search_fields = (
        "name",
        "theme",
        "venue",
    )

    list_filter = (
        "status",
        "start_date",
    )
    