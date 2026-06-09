from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from Equip.api.serializers2 import EquipsSerializer2
from Equip.models import Equip
from User.models import *


class PermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    permisos_data = PermisosSerializer(source='permisos', many=True, read_only=True)

    class Meta:
        model = Rol
        fields = ['id', 'nom', 'permisos', 'permisos_data']


class UserSerializer(serializers.ModelSerializer):
    rols_data = RolSerializer(source='rols', many=True, read_only=True)
    permisos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_fields = ['rols_data', 'permisos']

    def get_permisos(self, obj):
        permisos = set()
        for rol in obj.rols.all():
            for permis in rol.permisos.all():
                permisos.add(permis.nom)
        return list(permisos)


class UserSerializer3(serializers.ModelSerializer):
    rols_data = RolSerializer(source='rols', many=True, read_only=True)
    permisos = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']
        extra_fields = ['rols_data', 'permisos', 'equipos']

    def get_permisos(self, obj):
        permisos = set()
        for rol in obj.rols.all():
            for permis in rol.permisos.all():
                permisos.add(permis.nom)
        return list(permisos)




class RolUsuariSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    rol_data = RolSerializer(source='rol', read_only=True)

    class Meta:
        model = RolUsuari
        fields = ['id', 'rol', 'user', 'rol_data', 'user_data']


class UserSerializer2(serializers.ModelSerializer):
    equips_data = serializers.SerializerMethodField()
    rols_data = RolSerializer(source='rols', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_fields = ['rols_data']

    def get_equips_data(self, obj):
        equips_data = Equip.objects.filter(users__user=obj)
        serializer = EquipsSerializer2(equips_data, many=True)
        return serializer.data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'address', 'last_name', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        # Elimina el campo password_confirm del diccionario validated_data
        validated_data.pop('password_confirm', None)
        return super().create(validated_data)
