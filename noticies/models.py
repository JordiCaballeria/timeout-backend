from django.db import models

from Esdeveniment.models import Esdeveniment


class noticies(models.Model):
    titol = models.CharField(max_length=255)
    subtitol = models.CharField(max_length=255)
    path_imatge= models.ImageField(upload_to='noticies')
    contingut = models.TextField()
    esdeveniment = models.ForeignKey(Esdeveniment, on_delete=models.SET_NULL, null=True, blank=True)
    autor = models.CharField(max_length=50)
    fotograf = models.CharField(max_length=50)
    activa = models.BooleanField(default=True)
    nomes_jugadors = models.BooleanField(default=False)
    data_publicacio = models.DateTimeField(null=True)

    def __str__(self):
        return self.titol


