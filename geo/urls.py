from django.contrib import admin
from django.urls import path
from .views import Mapa,IndexView,search_assunto,DanoAmbiental

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('search',search_assunto,name='search_assunto'),
    path('dano',DanoAmbiental.as_view(),name='dano_ambiental'),
    path('mapa',Mapa.as_view(),name='mapa'),
]