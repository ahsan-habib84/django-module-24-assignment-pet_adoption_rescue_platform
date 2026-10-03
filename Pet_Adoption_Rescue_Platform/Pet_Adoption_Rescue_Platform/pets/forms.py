from django import forms
from .models import AdoptionRequest

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = [
            "address", "phone", "reason",
            "previous_pet_experience", "message"
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "reason": forms.Textarea(attrs={"rows": 4}),
            "message": forms.Textarea(attrs={"rows": 3}),
        }
