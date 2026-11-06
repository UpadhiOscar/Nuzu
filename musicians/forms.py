
from django import forms
from .models import MusicianProfile


class MusicianProfileForm(forms.ModelForm):
    class Meta:
        model = MusicianProfile
        exclude = [
            "user",
            "is_verified",
            "is_available",
            "created_at",
            "updated_at",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 200,
                "placeholder": "Tell clients about your musical experience..."
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "e.g. Port Harcourt"
            }),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get("bio", "")
        if len(bio) > 200:
            raise forms.ValidationError(
                "Your bio cannot exceed 200 characters."
            )
        return bio
