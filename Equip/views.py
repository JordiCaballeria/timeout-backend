from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Equip.api.serializers import EquipsSerializer
from Equip.models import Equip, EquipUsuaris
from TimeOut.permisos import HasEditarEquipsPermission
from User.models import RolUsuari

@api_view(['POST'])
@permission_classes([IsAuthenticated, HasEditarEquipsPermission])
def update_jugadors(request):
    equip_id = request.data.get('equip_id')
    users_ids = request.data.get('users_ids')

    equip = Equip.objects.get(id=equip_id)
    rol_usuaris_ids = RolUsuari.objects.filter(
        user__in=users_ids, rol__nom='Jugador/a'
    ).values_list('id', flat=True)

    equip_usuaris = EquipUsuaris.objects.filter(
        equip=equip, rolusuari__rol__nom='Jugador/a'
    )

    equip_usuaris_ids = set(equip_usuaris.values_list('rolusuari__id', flat=True))

    missing_ids_add = set(rol_usuaris_ids) - equip_usuaris_ids
    missing_ids_remove = equip_usuaris_ids - set(rol_usuaris_ids)

    for rol_usuari_id in missing_ids_add:
        user_id = RolUsuari.objects.get(id=rol_usuari_id)
        equip_usuari = EquipUsuaris(
            equip=equip, rolusuari=user_id
        )
        equip_usuari.save()

    for rol_usuari_id in missing_ids_remove:
        equip_usuari = equip_usuaris.get(rolusuari__id=rol_usuari_id)
        equip_usuari.delete()

    return Response({'success': True})
@api_view(['POST'])
@permission_classes([IsAuthenticated, HasEditarEquipsPermission])
def update_entrenadors(request):
    equip_id = request.data.get('equip_id')
    users_ids = request.data.get('users_ids')

    equip = Equip.objects.get(id=equip_id)
    rol_usuaris_ids = RolUsuari.objects.filter(
        user__in=users_ids, rol__nom='Entrenador/a'
    ).values_list('id', flat=True)

    equip_usuaris = EquipUsuaris.objects.filter(
        equip=equip, rolusuari__rol__nom='Entrenador/a'
    )

    equip_usuaris_ids = set(equip_usuaris.values_list('rolusuari__id', flat=True))

    missing_ids_add = set(rol_usuaris_ids) - equip_usuaris_ids
    missing_ids_remove = equip_usuaris_ids - set(rol_usuaris_ids)

    for rol_usuari_id in missing_ids_add:
        user_id = RolUsuari.objects.get(id=rol_usuari_id)
        equip_usuari = EquipUsuaris(
            equip=equip, rolusuari=user_id
        )
        equip_usuari.save()

    for rol_usuari_id in missing_ids_remove:
        equip_usuari = equip_usuaris.get(rolusuari__id=rol_usuari_id)
        equip_usuari.delete()

    return Response({'success': True})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def equip_client_id(request, equip_id):
    try:
        equip = Equip.objects.get(id=equip_id)
    except Equip.DoesNotExist:
        return Response(status=404)

    serializer = EquipsSerializer(equip)
    return Response(serializer.data)