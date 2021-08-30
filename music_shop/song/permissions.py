from rest_framework.permissions import BasePermission


class ModeratorPermission(BasePermission):
    message = "Sorry, You have no permission"

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator"):
            return True

        if request.user.is_superuser:
            return True
