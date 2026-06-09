import secrets

from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_soci", False)
        extra_fields.setdefault("is_active", False)

        if not username:
            raise ValueError('The user must have a username')

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(username, email, password, **extra_fields)

class Permisos(models.Model):
    nom = models.CharField(max_length=50)


class Rol(models.Model):
    nom = models.CharField(max_length=50)
    permisos = models.ManyToManyField(Permisos)


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=150,
        unique=True,

    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    path_photo = models.ImageField(upload_to='User', null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    account = models.CharField(max_length=100, blank=True)
    fitxa = models.CharField(max_length=100, blank=True)
    dorsal = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    activation_token = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_soci = models.BooleanField(
        default=False,

    )
    is_superuser = models.BooleanField(
        default=False,

    )
    date_finish_soci = models.DateTimeField(null=True)
    date_joined_soci = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    rols = models.ManyToManyField(Rol, through='RolUsuari')
    objects=UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email","password"]

    def __str__(self):
        return f'{self.username}'

    def has_perm(self,perm, obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    def generate_activation_token(self):
        token = secrets.token_urlsafe(32)
        self.activation_token = token
        self.save()
        return token


class RolUsuari(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_rol_usuari_ids(cls, user_ids):
        """
        Obtiene todas las ids de RolUsuari cuyo campo user coincida con alguna de las ids de User en el array.
        :param user_ids: Array de ids de User
        :return: Array de ids de RolUsuari
        """
        rol_usuari_ids = cls.objects.filter(user__in=user_ids).values_list('id', flat=True)
        return rol_usuari_ids