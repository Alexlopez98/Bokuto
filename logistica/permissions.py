from rest_framework.permissions import BasePermission

class IsBodeguero(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Bodeguero').exists())

class IsOperadorSala(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Operador_Sala').exists())

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Administrador').exists())