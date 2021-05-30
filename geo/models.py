from django.db import models
from django.contrib.gis.db import models


class Assuntos(models.Model):
    codigo = models.IntegerField(primary_key=True,blank=False,null=False)
    cod_pai = models.ForeignKey('self', null=True,blank=True,related_name='assuntos_pai',on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'Assuto'
        verbose_name_plural = 'Assuntos'
    
    def __str__(self):
        return str(self.codigo)+" "+self.descricao
    

class Area(models.Model):
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    cod_municipio_ibge = models.CharField(max_length=50,null=True,blank=True)
    municipio = models.CharField(max_length=60,null=True,blank=True)
    geo_m =models.CharField(max_length=1000)
    cod_sigef = models.CharField(max_length=50,null=True,blank=True)
    terrai_cod=models.CharField(max_length=50,null=True,blank=True)
    cod_floresta = models.CharField(max_length=50,null=True,blank=True)
   
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
    
    def __str__(self):
        return str(self.latitude)+" "+self.longitude
   
    

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'processos/{0}/{1}'.format(instance.numero,filename)


class Processo(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(primary_key=True,max_length=255)
    cod_municipio_ibge = models.CharField(max_length=50,null=True,blank=True,default=None)
    arquivo = models.FileField(upload_to=user_directory_path,null=True,blank=True,default=None)
    cod_sigef = models.CharField(max_length=50,null=True,blank=True,default=None)
    terrai_cod=models.CharField(max_length=50,null=True,blank=True,default=None)
    cod_floresta = models.CharField(max_length=50,null=True,blank=True,default=None)
    sicar = models.CharField(max_length=50,null=True,blank=True,default=None)
    sirenejud=models.CharField(max_length=50,null=True,blank=True,default=None)
    latitude=models.CharField(max_length=50,null=True,blank=True,default=None)
    longitude=models.CharField(max_length=50,null=True,blank=True,default=None)
        
    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
    
    def __str__(self):
        return "{0} {1} {2}".format(self.numero,self.sirenejud,self.sicar)
    
class DataJud(models.Model):
    numero = models.CharField(max_length=255, blank=True)
    sirenejud=models.CharField(max_length=50,null=True,blank=True,default=None)
    latitude=models.CharField(max_length=50,null=True,blank=True,default=None)
    longitude=models.CharField(max_length=50,null=True,blank=True,default=None)
    cod_sigef = models.CharField(max_length=50,null=True,blank=True,default=None)
    
    class Meta:
        verbose_name = 'DataJud'
        verbose_name_plural = 'DataJud'
        
    def __str__(self):
        return "{0} {1}".format(self.numero,self.sirenejud)
    
class Sicar(models.Model):
    sicar = models.CharField(max_length=50,null=True,blank=True,default=None)
    datajud = models.ForeignKey('DataJUD',on_delete=models.CASCADE)
    
    def __str__(self):
       return "{0} {1}".format(self.sicar,self.datajud)
    
    
