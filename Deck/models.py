from django.db import models
from django.contrib.auth.models import User


class Deck(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class FlashCard(models.Model):
    parte_frontal = models.TextField()
    parte_trasera = models.TextField()
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE, related_name='flashcards')

    def __str__(self):
        return f'{self.parte_frontal} - {self.parte_trasera}'
