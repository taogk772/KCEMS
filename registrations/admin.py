from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "registration_number",
        "first_name",
        "last_name",
        "event",
        "phone",
        "email",
        "registration_type",
        "registration_fee",
        "pledge",
        "created_at",
    )

    list_filter = (
        "event",
        "registration_type",
        "category",
        "gender",
    )

    search_fields = (
        "registration_number",
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    ordering = ("-created_at",)