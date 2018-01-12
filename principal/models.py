from django.db import models

class Categoria(models.Model):
    tipo = models.CharField(max_length=50)
    
    def __unicode__(self):
        return str(self.tipo)

class Producto(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    descripcion = models.CharField(max_length=500)
    categorias = models.ManyToManyField(Categoria)
    url = models.URLField()

    def __unicode__(self):
        return str(self.name)
