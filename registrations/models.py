from django.db import models


class Registration(models.Model):

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

    # Family members
    adults = models.PositiveIntegerField(default=0)
    youths = models.PositiveIntegerField(default=0)
    young_generation = models.PositiveIntegerField(default=0)

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

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def calculate_registration_fee(self):

        # Individual registration
        if self.registration_type == "individual":

            if self.category == "adult":
                return 20

            elif self.category == "youth":
                return 10

            elif self.category == "young":
                return 5

        # Family registration
        return (
            (self.adults * 20)
            + (self.youths * 10)
            + (self.young_generation * 5)
        )

    @property
    def grand_total(self):
        return self.registration_fee + self.pledge

    def save(self, *args, **kwargs):

        if not self.registration_number:

            last = Registration.objects.order_by('-id').first()

            if last and last.registration_number:
                last_number = int(last.registration_number.split('-')[-1])
            else:
                last_number = 0

            self.registration_number = f"AC2026-{last_number + 1:04d}"

        self.registration_fee = self.calculate_registration_fee()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"
    