from django.db import models


class Registration(models.Model):

    # --------------------
    # CHOICES
    # --------------------
    CATEGORY_CHOICES = [
        ('adult', 'Adult ($20)'),
        ('youth', 'Youth ($10)'),
        ('young', 'Young Generation ($5)'),
    ]

    REGISTRATION_TYPES = [
        ('individual', 'Individual'),
        ('family', 'Family'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # --------------------
    # BASIC INFO
    # --------------------
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

    # --------------------
    # REGISTRATION INFO
    # --------------------
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

    # --------------------
    # FAMILY STRUCTURE
    # --------------------
    adults = models.PositiveIntegerField(default=0)
    youths = models.PositiveIntegerField(default=0)
    young_generation = models.PositiveIntegerField(default=0)

    # --------------------
    # FINANCIALS
    # --------------------
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

    # --------------------
    # META
    # --------------------
    from django.utils import timezone

    created_at = models.DateTimeField(default=timezone.now)

    # --------------------
    # PRICING LOGIC
    # --------------------
    def calculate_registration_fee(self):

        ADULT_PRICE = 20
        YOUTH_PRICE = 10
        YOUNG_PRICE = 5

        # Individual registration
        if self.registration_type == "individual":

            if self.category == "adult":
                return ADULT_PRICE
            elif self.category == "youth":
                return YOUTH_PRICE
            elif self.category == "young":
                return YOUNG_PRICE

        # Family registration
        return (
            (self.adults or 0) * ADULT_PRICE +
            (self.youths or 0) * YOUTH_PRICE +
            (self.young_generation or 0) * YOUNG_PRICE
        )

    # --------------------
    # GRAND TOTAL (READ ONLY)
    # --------------------
    @property
    def grand_total(self):
        return (self.registration_fee or 0) + (self.pledge or 0)

    # --------------------
    # SAVE OVERRIDE
    # --------------------
    def save(self, *args, **kwargs):

        # Generate registration number
        if not self.registration_number:

            last = Registration.objects.order_by('-id').first()

            if last and last.registration_number:
                try:
                    last_number = int(last.registration_number.split('-')[-1])
                except:
                    last_number = 0
            else:
                last_number = 0

            self.registration_number = f"AC2026-{last_number + 1:04d}"

        # Always recalculate fee before saving
        self.registration_fee = self.calculate_registration_fee()

        super().save(*args, **kwargs)

    # --------------------
    # DISPLAY
    # --------------------
    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"