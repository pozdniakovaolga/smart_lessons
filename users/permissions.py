from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """Права доступа автора"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False
