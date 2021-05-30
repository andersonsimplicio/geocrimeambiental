import os, sys
import re
import textract 
import time


def read_pdf_to_txt(path="",nome=""):
    t1 = time.time()
    files =path
    cwd = os.getcwd()
    text = textract.process("{}".format(cwd+files), method='tesseract', encoding='utf-8')
    texto = text.decode('utf-8')
    tempoExec = time.time() - t1
    return texto
    