"""permissions for users app."""
from rest_framework import permissions

from users.choices import ROLE


class IsAdmin(permissions.IsAuthenticated):
    """The request is authenticated as a user and user is an Admin"""

    def has_permission(self, request, view):
        super(IsAdmin, self).has_permission(request, view)
        if ROLE.__getitem__("admin") in request.roles:
            return True
        else:
            return False