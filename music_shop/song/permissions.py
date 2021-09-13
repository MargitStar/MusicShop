from rest_framework.permissions import BasePermission


class ModeratorPermission(BasePermission):
    message = "Sorry, You have no permission"

    def has_permission(self, request, view):
        return request.user.group == "Moderator" or (
            request.user.is_admin and request.user.is_staff
        )
