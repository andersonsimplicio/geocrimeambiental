from django.contrib import admin
from .models import Assuntos,Area,Processo




class AsssuntosManager(admin.ModelAdmin):
    list_display=['codigo','cod_pai','descricao']
    search_fields=['codigo','descricao']


class AreaManager(admin.ModelAdmin):
    list_display=['latitude','longitude','municipio','cod_sigef','terrai_cod']
    search_fields=['municipio','cod_sigef','terrai_cod']
    
class ProcessoManager(admin.ModelAdmin):
    list_display=['numero','arquivo','data','cod_sigef','terrai_cod']
    search_fields=['numero']
    

# Register your models here.
admin.site.register(Assuntos,AsssuntosManager)
admin.site.register(Area,AreaManager)
admin.site.register(Processo,ProcessoManager)