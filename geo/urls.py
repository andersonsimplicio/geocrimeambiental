from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import Mapa,DanoAmbiental,geobrain

urlpatterns = [
    path('',DanoAmbiental.as_view(),name='dano_ambiental'),
    path('analise',geobrain,name='geobrain'),
    path('mapa',Mapa.as_view(),name='mapa'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)