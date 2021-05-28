from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from .models import Assuntos
from shapely.geometry import Polygon, MultiPolygon, Point
from geopandas import GeoSeries
import geopandas as gp
import os
import folium
import pandas as pd
import json


#
def add_categorical_legend(folium_map, title, colors, labels):
    '''
     Transforma um poligono z(3D) em 2D
    '''
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo


class IndexView(TemplateView):
    
    template_name = "geo/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



style1 = {'fillColor': 'ff1919', 'color': '#ff0000'}
style2 = {'fillColor': '#DAA520', 'color': '#006400'}

def filter(geometry,ponto):
    for poly in geometry:
            if poly.geom_type == 'Polygon':
               if ponto.within(poly) or poly.within(ponto):
                    mask = poly  
                    return mask             
            elif poly.geom_type == 'MultiPolygon':
                for p in poly:
                    if ponto.within(p) or p.within(ponto):
                        mask = poly
                        return mask 
    return None


    
def get_arvore(no):
    assunto = {}
    assunto['codigo'] = no.codigo
    descricao = no.descricao
    _codigo = int(no.cod_pai.codigo)
    while True:
        a = Assuntos.objects.get(codigo=_codigo)
        if a is not None:
            descricao=str(a.descricao)+" / "+descricao
            if a.cod_pai is not None:
                _codigo = int(a.cod_pai.codigo)
            else:
                break
        else:
            break
    assunto['descricao'] = descricao  
    return assunto

def busca_arvore(no=Assuntos,lista=[]):
    try:
        lista_filhos= Assuntos.objects.filter(cod_pai=no.codigo)
        if lista_filhos.exists():
            for i in lista_filhos:
                no = busca_arvore(i,lista)
                if no is not None:
                    lista.append(get_arvore(no))
        else:
            dado = get_arvore(no)
            lista.append(dado)
        
    except Exception as e:
        print(e)

def search_assunto(request):
    if request.method=="POST" and request.is_ajax:
     '''
        Função responsavél por buscar assuntos
    '''
    resp =[]   
    
    def isnumber(value):
        try:
            int(value)
        except ValueError:
            return False
        return True
    
    if request.method == 'POST' and request.is_ajax:
        
        _assunto = request.POST['assunto']
        if isnumber(_assunto):
            _assunto = ""
            _codigo = request.POST['assunto']
        else:
            _assunto = request.POST['assunto']
            
        if _assunto != "":
            busca = Assuntos.objects.filter(descricao__icontains=_assunto)  
            if busca.exists():
                for b in busca:
                    lista = []
                    busca_arvore(b,lista)
                    for filhos in lista:
                        resp.append({'codigo':filhos['codigo'],'descricao':filhos['descricao']})
            else:
                resp.append({00:'Assunto não encontrado'}) 
        else:
            try:
                a = get_object_or_404(Assuntos,codigo=_codigo)
                assuntoBusca={}
                assuntoBusca['codigo']=int(a.codigo)
                assuntoBusca['descricao']=str(a.descricao)
                assuntoBusca['cod_pai']=int(a.cod_pai.codigo)
                resp.append({'codigo':assuntoBusca['codigo'],'descricao':get_arvore(assuntoBusca)})
                    
            except Exception as e:
                resp.append({00:'Assunto não encontrado'})                                           
    return JsonResponse({'assuntos':resp})

class DanoAmbiental(TemplateView):
    template_name = "geo/dano.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Mapa(TemplateView):
    template_name = "geo/mapa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        florestas = gp.read_file('data/shp/MT.shp')
        municipios = gp.read_file('data/municipios/MT_Municipios_2020.shp')   
        sigef = gp.read_file('data/sigef/Sigef Brasil_MT.shp')
        ponto =Point(-56.33195815,-14.57322648)  
        florestas.geometry = convert_3D_2D(florestas.geometry)
        mask = []
        
        mask_floresta = filter(florestas['geometry'],ponto)   
        if mask_floresta is not None:   
            print('Floresta')          
            geo_floresta =florestas[florestas['geometry']==mask_floresta]                            
            print(geo_floresta)
        mask_cidade = filter(municipios['geometry'],ponto)
        
        if mask_cidade is not None:
            print('Cidade')
            geo_cidade = municipios[municipios['geometry']==mask_cidade]                  
            print(geo_cidade)
            
        mask_sigef = filter(sigef['geometry'],ponto)  
         
        if mask_sigef is not None:
            print('Sigef:')
            geo_sigef = sigef[sigef['geometry']==mask_sigef]                  
            print(geo_sigef['nome_area']) 
               
            
        m = folium.Map(location=[-15.5989, -56.0949 ],width=1000, height=600, zoom_start=5)
        m.add_child(folium.LatLngPopup())
        folium.Marker([-15.5989, -56.0949],icon=folium.Icon(color='red', icon='info-sign' ),popup="Mato Grosso Cuiabá").add_to(m)  
        
        if mask_floresta is not None:    
            folium.GeoJson(data=geo_floresta,style_function=lambda x:style2).add_to(m)
        
        folium.Marker([-14.57322648,-56.33195815],icon=folium.Icon(color='red', icon='tree',prefix='fa'),popup="Dano Ambiental").add_to(m)          
        if mask_cidade is not None:
            folium.GeoJson(data=geo_cidade["geometry"]).add_to(m) 
        
        if mask_sigef is not None:
            folium.GeoJson(data=geo_sigef["geometry"],style_function=lambda x:style1).add_to(m) 
            
        # cidade = str(geo_cidade['NM_MUN'].astype(str))    
        # forest = str(geo_floresta['nome'].astype(str))
        # m = add_categorical_legend(m, 'Legenda',
        #                      colors = ['green','blue'],
        #                    labels = ['TERRA INDIGENA NAMBIKWARA','Comodoro'])
        
        mapa = m._repr_html_()  
        context['mapa']=mapa
        return context