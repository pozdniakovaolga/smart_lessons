from rest_framework.permissions import BasePermission


class CoursePermissions(BasePermission):
    """Права доступа к курсу"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            if request.user.is_authenticated:
                return not request.user.is_moderator
        elif view.action in ['list', 'retrieve', 'update', 'partial_update']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by or request.user.is_moderator:
            return True
        return False


class IsModerator(BasePermission):
    """Права доступа модератора"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_permission(self, request, view):
        if request.user.is_moderator:
            return True
        return False


class IsOwner(BasePermission):
    """Права доступа автора"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by:
            return True
        return False
