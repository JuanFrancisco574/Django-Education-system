from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from Deck.forms import DeckForm
from Deck.models import Deck
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Devuelve la vista a la página principal de la aplicación
def home(request):
    context = {}
    context['form'] = DeckForm()

    # Si existen mensajes de sesión los obtenemos
    mensajes = messages.get_messages(request)

    # Separamos los mensajes de éxito y los de fallo
    context['mensajes_exito'] = []
    context['mensajes_fallo'] = []
    for mensaje in mensajes:
        if mensaje.tags == 'success':
            context['mensajes_exito'].append(mensaje)
        else:
            context['mensajes_fallo'].append(mensaje)
    
    # Si el usuario está autenticado extraemos todos sus Decks
    context['decks'] = {}
    if request.user.is_authenticated:
        context['decks'] = Deck.objects.filter(usuario=request.user)

    return render(request,'usuario/index.html',context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            # Hacemos el Login
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('usuario:home')  # Redirige a la página principal
    else:
        form = UserLoginForm()

    return render(request, 'usuario/login.html', {'form': form})


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Registramos al usuario y lo enviamos al Login
            form.save()
            return redirect('usuario:login')  # Redirige a la página de Login
    else:
        form = UserRegistrationForm()

    return render(request, 'usuario/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('usuario:home')


@login_required
def como_funciona_view(request):
    return render(request,'usuario/como_funciona.html')