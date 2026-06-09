from django.db import models
from Esdeveniment.models import *
from User.models import *


# Create your models here.
class Patrocinador(models.Model):
    nom = models.CharField(max_length=30)
    email = models.EmailField(null=False, blank=False)
    numCompte = models.CharField(max_length=50)
    telefon = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    path_imatge = models.ImageField(upload_to='patrocinadors')
    direccio = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True, default='')
    actiu = models.BooleanField(default=True)

