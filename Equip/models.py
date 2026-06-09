from django.db import models
from User.models import *

# Create your models here.
class Categoria(models.Model):
    nom = models.CharField(max_length=20)
class Divisio(models.Model):
    nom = models.CharField(max_length=20)
class Esport(models.Model):
    nom = models.CharField(max_length=30)
class Equip(models.Model):
    nom = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    esport = models.ForeignKey(Esport, on_delete=models.SET_NULL, null=True, blank=True) # Relació N..1 amb Esport
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True) # Relació n..1 amb Categoria
    divisio = models.ForeignKey(Divisio, on_delete=models.CASCADE, null=True, blank=True) # Relació N..1 amb Divisio
    users = models.ManyToManyField(RolUsuari, through='EquipUsuaris')
    # Relació 1..N amb Esdeveniment
class EquipUsuaris(models.Model):
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, null=True)
    rolusuari = models.ForeignKey(RolUsuari, on_delete=models.CASCADE, null=True)

    @classmethod
    def get_equip_usuaris_ids(cls, rolusuari_ids, equip_id):
        """
        Obtiene todas las ids almacenadas en el campo rolusuari de los registros de EquipUsuaris, donde el rol
        relacionado tenga el nom de "Jugador/a" y el equip sea el especificado por equip_id.
        :param rolusuari_ids: Array de ids de RolUsuari
        :param equip_id: Id del equip
        :return: Array de ids de RolUsuari en los registros de EquipUsuaris que cumplen los criterios
        """
        equip_usuaris_ids = cls.objects.filter(rolusuari__in=rolusuari_ids, equip=equip_id,
                                               rolusuari__rol__nom="Jugador/a").values_list('rolusuari', flat=True)
        return equip_usuaris_ids

    @classmethod
    def sync_equip_usuaris(cls, rol_usuari_ids, equip_usuaris_ids, equip_id):
        """
        Sincroniza los registros de EquipUsuaris con las ids de RolUsuari y EquipUsuaris pasadas como parámetros.
        Agrega un registro por cada id de RolUsuari que no esté en EquipUsuaris con la equip_id especificada,
        y elimina los registros de EquipUsuaris cuyo campo user esté en equip_usuaris_ids pero no en rol_usuari_ids.
        :param rol_usuari_ids: Array de ids de RolUsuari
        :param equip_usuaris_ids: Array de ids de EquipUsuaris
        :param equip_id: Id del equip
        """
        # Agregar registros por cada id de RolUsuari que no esté en EquipUsuaris
        rol_usuari_ids_not_in_equip_usuaris = list(set(rol_usuari_ids) - set(equip_usuaris_ids))
        equip_instance = Equip.objects.get(id=equip_id)  # Obtener la instancia de Equip basada en el equip_id
        for rol_usuari_id in rol_usuari_ids_not_in_equip_usuaris:
            rol_usuari = RolUsuari.objects.get(id=rol_usuari_id)
            cls.objects.create(equip=equip_instance,
                               rolusuari=rol_usuari)  # Pasar la instancia de Equip en lugar del equip_id

        # Eliminar registros de EquipUsuaris cuyo campo user esté en equip_usuaris_ids pero no en rol_usuari_ids
        equip_usuaris_ids_not_in_rol_usuari_ids= list(set(equip_usuaris_ids) - set(rol_usuari_ids))
        for equip_usuari_id in equip_usuaris_ids_not_in_rol_usuari_ids:
            rol_usuari = RolUsuari.objects.get(id=equip_usuari_id)
            cls.objects.get(equip=equip_instance, rolusuari=rol_usuari).delete()
