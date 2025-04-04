from django import forms

from films.forms import StyleFormMixin
from interactions.models import Interaction


class InteractionForm(forms.ModelForm, StyleFormMixin):
    """
    Форма взаимодействия (оценки).
    """
    class Meta:
        model = Interaction
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 5,
                    'step': 0.5
                }
            )
        }
