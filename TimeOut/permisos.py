from rest_framework import permissions

from TimeOut.utils import check_permission


class HasEnviarMailsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EnviarMails'
        return check_permission(user_id, permission_name)


class HasVeureEquipsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureEquips'
        return check_permission(user_id, permission_name)


class HasEditarEquipsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarEquips'
        return check_permission(user_id, permission_name)


class HasVeureJugadorsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureJugadors'
        return check_permission(user_id, permission_name)


class HasEditarJugadorsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarJugadors'
        return check_permission(user_id, permission_name)


class HasVeureCompeticioPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureCompeticio'
        return check_permission(user_id, permission_name)


class HasEditarCompeticioPErmission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarCompeticio'
        return check_permission(user_id, permission_name)


class HasVeureEsdevenimentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureEsdeveniments'
        return check_permission(user_id, permission_name)


class HasEditarEsdevenimentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarEsdeveniments'
        return check_permission(user_id, permission_name)


class HasVeureNoticiesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureNotices'
        return check_permission(user_id, permission_name)


class HasEditarNoticiesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarNoticies'
        return check_permission(user_id, permission_name)


class HasVeureBotigaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureBotiga'
        return check_permission(user_id, permission_name)


class HasEditarBotigaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarBotiga'
        return check_permission(user_id, permission_name)


class HasVeureUsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureUsers'
        return check_permission(user_id, permission_name)


class HasEditarUsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarUsers'
        return check_permission(user_id, permission_name)


class HasVeureRolsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureRols'
        return check_permission(user_id, permission_name)


class HasEditarRolsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarRols'
        return check_permission(user_id, permission_name)


class HasVeurePatrocinadorsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeurePatrocinadors'
        return check_permission(user_id, permission_name)


class HasEditarPatrocinadorsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarPatrocinadors'
        return check_permission(user_id, permission_name)


class HasVeurePagamentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureBotiga'
        return check_permission(user_id, permission_name)


class HasEditarPagamentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarBotiga'
        return check_permission(user_id, permission_name)


class HasVeureEntradesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureEntrades'
        return check_permission(user_id, permission_name)


class HasEditarEntradesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarEntrades'
        return check_permission(user_id, permission_name)


class HasVeureEnviamentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'VeureEnviaments'
        return check_permission(user_id, permission_name)


class HasEditarEnviamentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        permission_name = 'EditarEnviaments'
        return check_permission(user_id, permission_name)
