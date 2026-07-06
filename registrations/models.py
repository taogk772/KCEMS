from django.db import models
from django.utils import timezone


class Registration(models.Model):

    # =====================
    # CHOICES
    # =====================
    CATEGORY_CHOICES = [
        ('adult', 'Adult ($20)'),
        ('young', 'Young Generation ($10)'),
        ('sunday', 'Sunday School ($5)'),
    ]

    REGISTRATION_TYPES = [
        ('individual', 'Individual'),
        ('family', 'Family'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # =====================
    # BASIC INFO
    # =====================
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='male'
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    church = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE
    )

    # =====================
    # REGISTRATION INFO
    # =====================
    registration_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    registration_type = models.CharField(
        max_length=20,
        choices=REGISTRATION_TYPES,
        default='individual'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='adult'
    )

    # =====================
    # FAMILY INFO
    # =====================
    adults = models.PositiveIntegerField(default=0)
    young_generation = models.PositiveIntegerField(default=0)
    sunday_school = models.PositiveIntegerField(default=0)

    # =====================
    # FINANCIALS
    # =====================
    pledge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # =====================
    # META
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

        ADULT_PRICE = 20
        YOUNG_PRICE = 10
        SUNDAY_PRICE = 5

        if self.registration_type == "individual":

            if self.category == "adult":
                return ADULT_PRICE

            elif self.category == "young":
                return YOUNG_PRICE

            elif self.category == "sunday":
                return SUNDAY_PRICE

            return 0

        # Family Registration
        return (
            (self.adults or 0) * ADULT_PRICE +
            (self.young_generation or 0) * YOUNG_PRICE +
            (self.sunday_school or 0) * SUNDAY_PRICE
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

        # Generate Registration Number
        if not self.registration_number:

            last = Registration.objects.order_by('-id').first()

            if last and last.registration_number:
                try:
                    last_number = int(last.registration_number.split('-')[-1])
                except ValueError:
                    last_number = 0
            else:
                last_number = 0

            self.registration_number = f"AC2026-{last_number + 1:04d}"

        # Calculate registration fee
        self.registration_fee = self.calculate_registration_fee()

        super().save(*args, **kwargs)

    # =====================
    # STRING DISPLAY
    # =====================
    def __str__(self):
        return f"{self.registration_number} - {self.full_name}"