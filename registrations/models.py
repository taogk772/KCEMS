from django.db import models
from django.utils import timezone


class Registration(models.Model):

    # =====================
    # CHOICES
    # =====================
    CATEGORY_CHOICES = [
        ("adult", "Adult ($20)"),
        ("young_generation", "Young Generation ($10)"),
        ("sunday_school", "Sunday School ($5)"),
    ]

    REGISTRATION_TYPES = [
        ("individual", "Individual"),
        ("family", "Family"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    # =====================
    # BASIC INFORMATION
    # =====================
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="male",
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    church = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
    )

    # =====================
    # REGISTRATION DETAILS
    # =====================
    registration_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    registration_type = models.CharField(
        max_length=20,
        choices=REGISTRATION_TYPES,
        default="individual",
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="adult",
    )

    # =====================
    # FAMILY ATTENDEES
    # =====================
    adults = models.PositiveIntegerField(default=0)

    young_generation = models.PositiveIntegerField(default=0)

    sunday_school = models.PositiveIntegerField(default=0)

    # =====================
    # FINANCIAL DETAILS
    # =====================
    pledge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # =====================
    # DATE CREATED
    # =====================
    created_at = models.DateTimeField(default=timezone.now)

    # =====================
    # FULL NAME
    # =====================
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # =====================
    # REGISTRATION FEE
    # =====================
    def calculate_registration_fee(self):

        adult_price = 20
        young_generation_price = 10
        sunday_school_price = 5

        if self.registration_type == "individual":

            if self.category == "adult":
                return adult_price

            if self.category == "young_generation":
                return young_generation_price

            if self.category == "sunday_school":
                return sunday_school_price

            return 0

        return (
            (self.adults or 0) * adult_price
            + (self.young_generation or 0) * young_generation_price
            + (self.sunday_school or 0) * sunday_school_price
        )

    # =====================
    # GRAND TOTAL
    # =====================
    @property
    def grand_total(self):
        return (self.registration_fee or 0) + (self.pledge or 0)

    # =====================
    # SAVE
    # =====================
    def save(self, *args, **kwargs):

        if not self.registration_number:

            last_registration = Registration.objects.order_by("-id").first()

            if last_registration and last_registration.registration_number:
                try:
                    last_number = int(
                        last_registration.registration_number.split("-")[-1]
                    )
                except (ValueError, IndexError):
                    last_number = 0
            else:
                last_number = 0

            self.registration_number = (
                f"AC2026-{last_number + 1:04d}"
            )

        self.registration_fee = self.calculate_registration_fee()

        super().save(*args, **kwargs)

    # =====================
    # DISPLAY
    # =====================
    def __str__(self):
        return f"{self.registration_number} - {self.full_name}"