# -*- coding: utf-8 -*-
"""regex_busca_codigos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fS8E1kyxnvz7Sw4LMSb865Th1c5SJVa9
"""

import pandas as pd
import numpy as np
import os
import re

"""Cria uma lista para armazenar os nomes dos arquivos

"""

files = []
pasta = '/content/processos' # diretorio com os arquivos

# funcao para ler todos os arquivos e deixar em uma lista
# param @pasta -> diretório onde estão os arquivos a serem processados
def lista_arquivos (pasta) :
  for diretorio, subpastas, arquivos in os.walk(pasta):
      for arquivo in arquivos:
          files.append(os.path.join(diretorio, arquivo))
          '\n'.join(files)
  return files

arquivos = lista_arquivos(pasta)

# funcao para ler lista de arquivos e
# gerar o dataframe com os códigos encontratos
# param @arquivo -> diretório dos arquivos

def busca_sigef(texto) :

  data = {}

  df = pd.DataFrame (columns = ['SIGEF','CAR'])
  
  sigef = re.findall(r'\b\d{13}\b', texto)
  car = re.findall("[A-Z]{2}-\d{7}-[A-Z0-9]{32}", texto)
  if sigef is None:
        sigef=""
  if car is None:
        car=""
  
  data = {'SIGEF':sigef,'CAR':car}
  return data
  
# exporta para CSV
#from google.colab import files
#df_codes.to_excel('codes.xlsx') 
#files.download('codes.xlsx')