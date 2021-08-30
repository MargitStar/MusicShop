from rest_framework.permissions import BasePermission


class ModeratorPermission(BasePermission):
    message = "Sorry, You have no permission"

    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name="Moderator")) or request.user.is_superuser
