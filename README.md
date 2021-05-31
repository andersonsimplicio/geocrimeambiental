![logo](https://user-images.githubusercontent.com/37173966/120087481-d08aab00-c0be-11eb-85af-0202b0f24bd3.jpeg)<a href="http://mapajud.pjexperience.com.br">MapaJud</a>

# MapaJud   
LIODS CNJ - Inovação, Inteligência e Objetivos de Desenvolvimento Sustentável


[![Build Status](https://travis-ci.org/googlemaps/google-maps-services-python.svg?branch=master)](https://travis-ci.org/googlemaps/google-maps-services-python)
[![PyPI version](https://badge.fury.io/py/googlemaps.svg)](https://badge.fury.io/py/googlemaps)


# Sumário
1. [Introdução](#introducao)
2. [Especificações](#especificacoes)
3. [Por que Usar?](#porqueusar)
4. [Perguntas Frequentes](#perguntasfrequentes)
5. [Sobre](#sobre)
6. [Licenças](#licencas)


## Introdução
  MapaJud indexa o número único do processo de terras públicas ao código do SireneJud exibindo inclusive outras bases de dados de georreferenciamento como INCRA, 
 Sistema de Gestão Fundiária (SIGEF), Cadastro Ambiental Rural (CAR), Serviço Florestal Brasileiro (SFB), e se aprenta como demonstrado da figura.
 
 ![tela_Inicial](https://user-images.githubusercontent.com/37173966/120129204-eb7e1d80-c199-11eb-863a-42111f7d8217.png)

## Especificações
1. MapaJud é capaz de vincular a uma área os códigos do SIGEF, CAR, SireneJud, se houver. 
2. Lê as peças processuais e extrai dados como: SIGEF e CAR e relaciona estes códigos com os já regitrados na base dos poligonos, tornando possível georreferenciar o local apresentado na peça processual, vinculando o número do processo à área objeto da ação. 
3. Com a leitura das peças, o MapaJud é capaz de indicar a localização geográfica em um mapa e listar os processos envolvendo a área alvo, apontando todos os códigos cadastrados na área traçada pelo polígono, incluindo o código SireneJud.  Por se tratar de um protótipo e para não sobrecarregar o tempo de excução do MapaJud convertemos os pdf em txt para então fazer a leitura das informações necessária para a integração da base de dados. 
4. Sua arquitetura esta descrita na figura a seguir:

![arquitetura (1)](https://user-images.githubusercontent.com/37173966/120129753-ec637f00-c19a-11eb-8df2-be6a9f7fde69.jpeg)

## Por que usar?
O MapaJud auxilia não só o poder judiciário, como também as instituições envolvidas com a manutenção, melhoria e proteção do meio ambiente. Uma vez que a aplicação converge todos os códigos, podendo cruzar informações relevantes sobre áreas públicas. Além de indicar a reicidência de danos ou crimes cometidos no poligono. Uma breve apresentação da ferramenta pode ser vista no <a href="https://www.youtube.com/watch?v=3l81MM-RJDg">video</a>.


## Perguntas Frequentes
O MapaJud foi inspirado em algum outro projeto?

Não, a ideia é totalmente inovadora tendo subsidio básico com o i3Geo do INCRA. 


É possivel implentar o MapaJud ao meu aplicativo?

Sim, nós desenvolvemos uma API que poderá ser consumida em qualquer aplicação python tanto para visualização quanto para fins de exploração de dados usando técnicas de predição. 

## Sobre
O MapaJud foi desenvolvido pela equipe interdiciplinar orientada pelo desafio 2 do Hackathon Liods/CNJ envolvendos colaboradores da área juridica, desenvolvedores programação e da inteligência artificial.  Para acessa basta clicar em <a href="http://mapajud.pjexperience.com.br">MapaJud</a>.

## Licenças
 O desenvolvimento do MapaJud utilizou em sua integralidade aplicações livre Open Source como: 
 
 <a href="https://github.com/python-visualization/folium/blob/master/LICENSE.txt">Folium</a>
 
 <a href="https://github.com/geopandas/geopandas/blob/master/LICENSE.txt">Geopandas</a>
 
 <a href="https://github.com/dbashford/textract/blob/master/LICENSE">Textract</a>
 
 <a href="https://docs.python.org/3/license.html">Python</a>
 
 <a href="https://www.gnu.org/licenses/licenses.pt-br.html">HTML, CSS e JavaScript </a>


