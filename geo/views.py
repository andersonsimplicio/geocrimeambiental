from django.shortcuts import get_object_or_404, redirect,get_list_or_404
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from numpy.lib.twodim_base import mask_indices
from numpy.testing._private.utils import break_cycles
from .models import Assuntos,DataJud,Processo
from shapely.geometry import Polygon, MultiPolygon, Point
import random
from datetime import date
import geopandas as gp
import pandas as pd
import os
import folium
from .convert_pdf import read_pdf_to_txt
from .busca_codigos import busca_sigef
pd.set_option('display.max_columns', None)
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
style2 = {'fillColor': 'green', 'color': 'green'}
style3 = {'fillColor': '#9c5010', 'color': 'orange'}
style4 = {'fillColor': '#FFFF00', 'color': '#483D8B'}

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
        _numero = self.request.session['processo']
        m = folium.Map(location=[-15.5989, -56.0949 ],width=735, height=437, zoom_start=5)
        p =None
        try:
           p =get_object_or_404(Processo,numero=_numero)
        except:
            pass
        historico =""
        florestas = gp.read_file('data/Florestas/MT_floresta_SireneJud.shp')
        municipios = gp.read_file('data/municipios/MT_Municipios_2020.shp')   
        sigef = gp.read_file('data/sigef/Sigef Brasil_MT.shp')
        area_imovel = gp.read_file('data/area/AREA_IMOVEL.shp')
        terra_indigena = gp.read_file('data/terra_indigena/ti_sirgas.shp')
        app = gp.read_file('data/app/APP.shp')
        app_alto = gp.read_file('data/app_altoParaguai/APP.shp')
        
        florestas.geometry = convert_3D_2D(florestas.geometry)
        mask = []  
        mask_floresta = None 
        mask_cidade = None
        mask_area_imovel = None
        mask_indigena = None
        mask_sigef = None
        mask_app = None
        mask_app_alto =None
        geo_floresta = None
        if p.latitude is not None and p.longitude is not None:	 
            try:   
                latitude=float(p.latitude)
                longitude=float(p.longitude)
                ponto =Point(longitude,latitude) 
                mask_floresta = filter(florestas['geometry'],ponto) 
                mask_cidade = filter(municipios['geometry'],ponto)
                mask_area_imovel = filter(area_imovel['geometry'],ponto)
                mask_indigena = filter(terra_indigena['geometry'],ponto)
                mask_sigef = filter(sigef['geometry'],ponto) 
                mask_app = filter(app['geometry'],ponto) 
                mask_app_alto =filter(app_alto['geometry'],ponto)
                folium.Marker([latitude,longitude],icon=folium.Icon(color='red', icon='tree',prefix='fa'),popup="Dano Ambiental").add_to(m)
            except ValueError:
                sirene = p.sirenejud
                if sirene is not None:
                    geo_floresta = florestas[florestas['SireneJud']==sirene] 
        else:
            sirene = p.sirenejud
            if sirene is not None:
                geo_floresta = florestas[florestas['SireneJud']==sirene]
       
        if mask_app is not None:           
            geo_app =app[app['geometry']==mask_app]                            
                    
        if mask_app_alto is not None:            
            geo_app_a =app_alto[app_alto['geometry']==mask_app_alto]                            
        
        if mask_floresta is not None:     
            geo_floresta =florestas[florestas['geometry']==mask_floresta]                            
            
        if mask_app is not None:
            geo_app = geo_app[geo_app['geometry']==mask_app]
        if mask_cidade is not None:
            geo_cidade = municipios[municipios['geometry']==mask_cidade]           
        
        
        if mask_area_imovel is not None:
            geo_area_imovel = area_imovel[area_imovel['geometry']==mask_area_imovel]                  
            car = geo_area_imovel['COD_IMOVEL'].values[0]
            historico = ""
                
        if mask_indigena is not None:
            geo_indigena = terra_indigena[terra_indigena['geometry']==mask_indigena]
                 
        if mask_sigef:
            geo_sigef = sigef[sigef['geometry']==mask_sigef]   

        folium.Marker([-15.5989, -56.0949],icon=folium.Icon(color='red', icon='info-sign' ),popup="Mato Grosso Cuiabá").add_to(m)  
        label =[]  
        cores =[]  
        
        if mask_floresta is not None:    
            folium.GeoJson(data=geo_floresta["geometry"],style_function=lambda x:style2).add_to(m)
            forest = str(geo_floresta['nome'].values[0])
            cores.append('green')
            label.append("Floresta: "+forest)
            if geo_floresta['SireneJud'].values[0] is not None:
                cores.append('#2F4F4F')
                label.append("SireneJud: "+str(geo_floresta['SireneJud'].values[0]))
            
        elif geo_floresta is not None:
            try:
                folium.GeoJson(data=geo_floresta['geometry'],style_function=lambda x:style2).add_to(m)
                forest = str(geo_floresta['nome'].values[0])
                cores.append('green')
                label.append("Floresta: "+forest)
                cores.append('#2F4F4F')
                if geo_floresta['SireneJud'].values[0] is not None:
                    label.append("SireneJud: "+str(geo_floresta['SireneJud'].values[0]))
                    sirene = str(geo_floresta['SireneJud'].values[0])
                    try: 
                        datajud = get_list_or_404(DataJud,sirenejud=sirene)
                        for data in datajud:
                            print(data.numero)
                            print(sirene)
                            if data.sirenejud == sirene:
                                historico+=str(data.numero)
                        context['historico']=historico 
                    except:
                        pass
            except IndexError:
                pass
            
        if mask_app is not None:    
            folium.GeoJson(data=geo_app["geometry"],style_function=lambda x:style2).add_to(m)
            app = str(geo_app['NOM_TEMA'].values[0])
            cores.append('#90EE90')
            label.append("APP "+app)
            
        if mask_app_alto is not None:    
            folium.GeoJson(data=geo_app_a["geometry"],style_function=lambda x:style2).add_to(m)
            app_a = str(geo_app_a['NOM_TEMA'].values[0])
            cores.append('#90EE90')
            label.append("APP "+app_a)
            
        if mask_cidade is not None:
            folium.GeoJson(data=geo_cidade["geometry"]).add_to(m) 
            cidade = str(geo_cidade['NM_MUN'].values[0])  
            cores.append('blue')
            label.append("Cidade "+cidade)
            
        if mask_sigef is not None:
            folium.GeoJson(data=geo_sigef["geometry"],style_function=lambda x:style1).add_to(m) 
            sigef = str(geo_sigef['codigo_imo'].values[0])
            cores.append('red')
            label.append("SIGEF: "+sigef)
            
        if mask_area_imovel is not None:
            folium.GeoJson(data=geo_area_imovel["geometry"],style_function=lambda x:style3).add_to(m)
            Car = str(geo_area_imovel['COD_IMOVEL'].values[0])
            cores.append('orange')
            label.append("Car: "+Car)
            
        if mask_indigena is not None:
            folium.GeoJson(data=geo_indigena["geometry"],style_function=lambda x:style4).add_to(m) 
            tribo = str(geo_indigena['terrai_nom'].values[0])  
            cores.append('#FFFF00')
            label.append("TI "+tribo)
                  
        m = add_categorical_legend(m, 'Legenda',
                             colors = cores,
                           labels = label)
        
        mapa = m._repr_html_()  
        context['mapa']=mapa
        return context


def gerarCodigoProcesso():
    data_atual = date.today()
    numero=""
    for i in range(7):
        numero+=str(random.randrange(9))
        
    for i in range(2):
        numero+=str(random.randrange(9))
    numero+=data_atual.strftime('%Y')
    return numero+str(random.randrange(9))+"08"+"0029"

    
def geobrain(request):
    if request.method=="POST":
        _numero = gerarCodigoProcesso()
        request.session['processo'] =_numero
        try:
            if request.FILES['file']:
                p = Processo.objects.create(
                numero = _numero,
                arquivo = request.FILES['file']
                )
                arquivo = request.FILES['file']
                texto = read_pdf_to_txt(p.arquivo.url,arquivo.name)           
                df = busca_sigef(texto=texto,numero_processo=_numero)
                if df is not None:
                    p.cod_sigef = df['sigef']
                    p.sicar=df['car']
            else:
                p = Processo.objects.create(numero = _numero,) 
        except:
            p = Processo.objects.create(numero = _numero,)           

        try:
           ibge = request.POST['ibge']  
           p.cod_municipio_ibge = ibge 
        except:
            pass
        try:
           sirene = request.POST['sirenejud']  
           p.sirenejud = sirene 
        except:
            pass
        try:
           sigef = request.POST['sigef']  
           p.cod_sigef = sigef
        except:
            pass
        try:
           longitude = request.POST['longitude']  
           latitude = request.POST['latitude']  
           p.latitude =latitude
           p.longitude=longitude
        except:
            pass
        
        p.save()
        
    return redirect('geo:mapa')
