from django.db import models
from Equip.models import Equip
# Create your models here.
class TipusEsdeveniment(models.Model):
    nom = models.CharField(max_length=30)
    descripcio = models.CharField(max_length=200)


class Esdeveniment(models.Model):
    nom = models.CharField(max_length=150)
    descripcio = models.CharField(max_length=400)
    tipusEsdeveniment = models.ForeignKey(TipusEsdeveniment, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=150, null=True)
    equip = models.ForeignKey(Equip, related_name="esdeveniments", on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(null=True)
    num_entrades= models.DecimalField(max_digits=5, decimal_places=0, default=0)
    num_entrades_disponibles= models.DecimalField(max_digits=5, decimal_places=0, default=0)
    preu_entrades=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    preu_entrades_soci=models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.nom


