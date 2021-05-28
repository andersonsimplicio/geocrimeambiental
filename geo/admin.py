from django.contrib import admin
from .models import Assuntos




class AsssuntosManager(admin.ModelAdmin):
    list_display=['codigo','cod_pai','descricao']
    search_fields=['codigo','descricao']
    

# Register your models here.
admin.site.register(Assuntos,AsssuntosManager)