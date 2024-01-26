from django.urls import path
from .views import agregar_deck,eliminar_deck,ver_flashcards,agregar_flashcard,eliminar_flashcard,estudiar_deck,terminar_estudio


app_name = 'Deck'

urlpatterns = [
    path('add/', agregar_deck, name='agregar_deck'),
    path('delete/<int:deck_id>/', eliminar_deck, name='eliminar_deck'),
    path('<int:deck_id>/flashcards/', ver_flashcards, name='ver_flashcards'),
    path('<int:deck_id>/flashcards/add/', agregar_flashcard, name='agregar_flashcard'),
    path('<int:deck_id>/flashcards/delete/<int:flashcard_id>/', eliminar_flashcard, name='eliminar_flashcard'),
    path('<int:deck_id>/flashcards/estudiar/', estudiar_deck, name='estudiar_deck'),
    path('<int:deck_id>/flashcards/estudiar/terminar/', terminar_estudio, name='terminar_estudio'),
    
]
