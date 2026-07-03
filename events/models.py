from django.db import models


class Event(models.Model):

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    theme = models.CharField(max_length=300)

    description = models.TextField()

    venue = models.CharField(max_length=250)

    start_date = models.DateField()
    end_date = models.DateField()

    registration_open = models.DateField()
    registration_close = models.DateField()

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    capacity = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    