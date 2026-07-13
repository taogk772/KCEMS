from django import forms

from .models import Registration


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration

        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "phone",
            "church",
            "address",
            "registration_type",
            "category",
            "adults",
            "young_generation",
            "sunday_school",
            "pledge",
        ]

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "gender": "Gender",
            "email": "Email Address",
            "phone": "Phone Number",
            "church": "Church",
            "address": "Address",
            "registration_type": "Registration Type",
            "category": "Individual Category",
            "adults": "Adults",
            "young_generation": "Young Generation",
            "sunday_school": "Sunday School",
            "pledge": "Pledge",
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Enter last name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter email address"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Enter phone number"}
            ),
            "church": forms.TextInput(
                attrs={"placeholder": "Enter church name"}
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Enter address"}
            ),
            "adults": forms.NumberInput(
                attrs={"min": 0}
            ),
            "young_generation": forms.NumberInput(
                attrs={"min": 0}
            ),
            "sunday_school": forms.NumberInput(
                attrs={"min": 0}
            ),
            "pledge": forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            ),
        }