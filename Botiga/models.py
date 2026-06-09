from django.db import models
from Esdeveniment.models import *
from User.models import *


# Create your models here.
class TipusProducte(models.Model):
    nom = models.CharField(max_length=30)


class Talles(models.Model):
    nom = models.CharField(max_length=80)


class Producte(models.Model):
    preu = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    preu_soci = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    nom = models.CharField(max_length=80)
    descripcio = models.TextField(max_length=350, null=False)
    tipusProducte = models.ForeignKey(TipusProducte, on_delete=models.CASCADE)
    actiu = models.BooleanField(default=True)


class ProducteTalles(models.Model):
    talla = models.ForeignKey(Talles, on_delete=models.CASCADE)
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    quantitat = models.DecimalField(max_digits=3, decimal_places=0)


class ImatgesProducte(models.Model):
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    path_imatge = models.ImageField(upload_to='productes')


class TipusPagament(models.Model):
    nom = models.CharField(max_length=30)


class Pagament(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    tipuspagament = models.ForeignKey(TipusPagament, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class DetallsPagament(models.Model):
    pagament = models.ForeignKey(Pagament, on_delete=models.CASCADE)
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talles, on_delete=models.SET_NULL, null=True)
    quantitat = models.DecimalField(max_digits=3, decimal_places=0, default=0)

class Entrada(models.Model):
    esdeveniment = models.ForeignKey(Esdeveniment, on_delete=models.CASCADE)  # Realció N..1 amb Esdeveniments
    pagament = models.ForeignKey(Pagament, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)
    codi = models.CharField(max_length=50, default='a')

class EstatEnviament(models.Model):
    nom = models.CharField(max_length=30)

class Enviament(models.Model):
    pagament = models.ForeignKey(Pagament, on_delete=models.CASCADE)
    direccio = models.CharField(max_length=200)
    estatenviament= models.ForeignKey(EstatEnviament, on_delete=models.SET_NULL, null=True)