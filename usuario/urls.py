from django.urls import path
from .views import user_login, user_registration, home, logout_view, como_funciona_view

app_name = 'usuario'

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', user_registration, name='register'),
    path('logout/', logout_view, name='logout'),
    path('como_funciona/', como_funciona_view, name='como_funciona'),
]
