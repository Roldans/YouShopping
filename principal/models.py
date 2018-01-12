from django.db import models

class Producto(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    descripcion = models.CharField(max_length=500)
    campos = models.CharField(max_length=50)
    url = models.URLField()

    def __unicode__(self):
        return str(self.name)