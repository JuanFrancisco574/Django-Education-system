from django import forms
from .models import Deck, FlashCard


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['nombre']

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre del nuevo Deck",
                }
            ),
            "usuario": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre del nuevo Deck",
                }
            ),
        }


class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ['parte_frontal', 'parte_trasera']

        widgets = {
            "parte_frontal": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "parte_trasera": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }
