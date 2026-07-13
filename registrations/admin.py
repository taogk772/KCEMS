from django.contrib import admin
from django.db.models import Sum

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "registration_number",
        "full_name",
        "event",
        "registration_type",
        "category_display",
        "adults_count",
        "young_generation_count",
        "sunday_school_count",
        "total_people",
        "registration_fee",
        "pledge",
        "created_at",
    )

    list_filter = (
        "event",
        "registration_type",
        "category",
        "gender",
        "created_at",
    )

    search_fields = (
        "registration_number",
        "first_name",
        "last_name",
        "email",
        "phone",
        "church",
    )

    ordering = ("-created_at",)

    @admin.display(description="Name")
    def full_name(self, obj):
        return obj.full_name

    @admin.display(description="Category")
    def category_display(self, obj):
        if obj.registration_type == "family":
            return "Family"
        return obj.get_category_display()

    @admin.display(description="Adults")
    def adults_count(self, obj):
        if obj.registration_type == "family":
            return obj.adults
        return 1 if obj.category == "adult" else 0

    @admin.display(description="Young Generation")
    def young_generation_count(self, obj):
        if obj.registration_type == "family":
            return obj.young_generation
        return 1 if obj.category == "young_generation" else 0

    @admin.display(description="Sunday School")
    def sunday_school_count(self, obj):
        if obj.registration_type == "family":
            return obj.sunday_school
        return 1 if obj.category == "sunday_school" else 0

    @admin.display(description="Total People")
    def total_people(self, obj):
        if obj.registration_type == "family":
            return (
                (obj.adults or 0)
                + (obj.young_generation or 0)
                + (obj.sunday_school or 0)
            )

        return 1

    def changelist_view(self, request, extra_context=None):

        totals = Registration.objects.aggregate(
            total_adults=Sum("adults"),
            total_young_generation=Sum("young_generation"),
            total_sunday_school=Sum("sunday_school"),
            total_fees=Sum("registration_fee"),
            total_pledges=Sum("pledge"),
        )

        extra_context = extra_context or {}

        extra_context.update({
            "total_adults": totals["total_adults"] or 0,
            "total_young_generation": totals["total_young_generation"] or 0,
            "total_sunday_school": totals["total_sunday_school"] or 0,
            "total_fees": totals["total_fees"] or 0,
            "total_pledges": totals["total_pledges"] or 0,
        })

        return super().changelist_view(
            request,
            extra_context=extra_context,
        )