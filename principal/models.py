from django.db import models

class Producto(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    descripcion = models.CharField(max_length=500)
    categorias = models.CharField(max_length=500)
    url = models.URLField()

    def __unicode__(self):
        return str(self.name)
