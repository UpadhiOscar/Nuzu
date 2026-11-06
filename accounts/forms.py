
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=20,
        required=False,
    )

    ACCOUNT_CHOICES = [
        ("hire", "I want to hire musicians"),
        ("provide", "I want to provide music services"),
        ("both", "Both — I want to hire and provide services"),
    ]

    account_type = forms.ChoiceField(
        choices=ACCOUNT_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "account_type",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]

        account_type = self.cleaned_data["account_type"]
        user.can_hire = account_type in ("hire", "both")
        user.can_provide_services = account_type in ("provide", "both")

        if commit:
            user.save()

        return user

