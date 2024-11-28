from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, FlashCardForm
from django.shortcuts import redirect
from .models import Deck, FlashCard
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def agregar_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        form.instance.usuario = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha creado el Deck exitosamente!')
        else:
            messages.error(
                request, 'No se pudo crear el Deck. Asegurate de ingresar datos correctos.')
    else:
        messages.error(request, 'Método inválido')

    return redirect('usuario:home')  # Redirige a la página principal


@login_required
def eliminar_deck(request, deck_id):
    # Válido que el Deck que se quiere eliminar sea del usuario que lo creo, es decir, un usuario no puede eliminar
    # un Deck que no le pertenezca.
    deck = Deck.objects.filter(usuario=request.user, id=deck_id)
    if deck.exists():
        # Borramos el Deck
        deck.delete()
        messages.success(request, 'Se ha eliminado el Deck!')
    else:
        messages.error(request, 'Acción no permitida')

    return redirect('usuario:home')  # Redirige a la página principal

# Esta vista muestra las FlashCards de un Deck en específico


@login_required
def ver_flashcards(request, deck_id):
    # Válido que el usuario que quiere ver las FlashCards del Deck sea el dueño del Deck.
    deck = get_object_or_404(Deck, id=deck_id, usuario=request.user)

    # Obtengo las FlashCards del Deck
    context = {}
    context['flashcards'] = FlashCard.objects.filter(deck=deck)
    context['deck'] = deck
    context['form'] = FlashCardForm()
    return render(request, 'Deck/CRUD_flashcards.html', context)


@login_required
def agregar_flashcard(request, deck_id):
    if request.method == 'POST':
        # Válido que la FlashCard que quiere agregar el usuario sea para un Deck del cual el usuario es el dueño
        deck = get_object_or_404(Deck, id=deck_id, usuario=request.user)

        # Agrego la FlashCard al Deck
        form = FlashCardForm(request.POST)
        form.instance.deck = deck
        if form.is_valid():
            form.save()
    # Redirige a la vista para ver las FlashCards
    url_destino = reverse('Deck:ver_flashcards', kwargs={'deck_id': deck.id})
    return redirect(url_destino)


@login_required
def eliminar_flashcard(request, deck_id, flashcard_id):
    # Valido que el Deck sea del usuario
    deck = get_object_or_404(Deck, id=deck_id, usuario=request.user)

    # Eliminamos la FlashCard
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    flashcard.delete()

    # Redirige a la vista para ver las FlashCards
    url_destino = reverse('Deck:ver_flashcards', kwargs={'deck_id': deck_id})
    return redirect(url_destino)

# Permite que el usuario pueda estudiar un Deck


@login_required
def estudiar_deck(request, deck_id):
    # Verifico que el deck que se quiere estudiar le pertenezca al usuario que lo quiere estudiar
    deck = get_object_or_404(Deck, id=deck_id, usuario=request.user)

    # Obtengo todas las flashcards del deck
    flashcards = FlashCard.objects.filter(deck=deck)

    # Creo una paginiación para estudiar el deck
    paginator = Paginator(flashcards, 1)

    # Se obtiene el número de flashcard de la solicitud GET, o 1 si no está presente
    pagina = request.GET.get('pagina', 1)

    try:
        flashcard_objects = paginator.page(pagina)
    except PageNotAnInteger:
        # Si la flashcard no es un número entero, muestra la primera flashcard
        flashcard_objects = paginator.page(1)
    except EmptyPage:
        # Si la flashcard está fuera de rango (por encima del número total de flashcards),
        # muestra la última flashcards disponible
        flashcard_objects = paginator.page(paginator.num_pages)

    context = {}
    context['deck'] = deck
    context['flashcard_objects'] = flashcard_objects
    return render(request, 'Deck/estudiar_deck.html', context)


# Esta vista termina el estudio del Deck y redirige a la vista que lista las FlashCards
@login_required
def terminar_estudio(request, deck_id):
    # Valido que al Deck que se vaya a redirigir sea un Deck del cual el usuario sea el dueño
    deck = get_object_or_404(Deck, id=deck_id, usuario=request.user)

    # Redirige a la vista para ver las FlashCards
    url_destino = reverse('Deck:ver_flashcards', kwargs={'deck_id': deck.id})
    return redirect(url_destino)
