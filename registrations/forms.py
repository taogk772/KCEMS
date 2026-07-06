from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = [
            'first_name',
            'last_name',
            'gender',
            'email',
            'phone',
            'church',
            'address',
            'registration_type',
            'category',

            # Family fields
            'adults',
            'young_generation',
            'sunday_school',

            'pledge',
        ]
        