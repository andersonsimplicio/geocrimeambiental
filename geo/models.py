from django.db import models


class Assuntos(models.Model):
    codigo = models.IntegerField(primary_key=True,blank=False,null=False)
    cod_pai = models.ForeignKey('self', null=True,blank=True,related_name='assuntos_pai',on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'Assuto'
        verbose_name_plural = 'Assuntos'
    
    def __str__(self):
        return str(self.codigo)+" "+self.descricao
    


    
