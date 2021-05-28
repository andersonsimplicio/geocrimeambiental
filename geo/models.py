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
    

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
    
    
