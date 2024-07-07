from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsNotDathVader(permissions.BasePermission):
    """
    Custom permission class to deny access to Darth Vader.

    This permission denies access to Darth Vader by checking if the user is authenticated
    and has the username 'darthvader'. If so, a PermissionDenied exception is raised with
    a specific message.

    Attributes:
    - request: The HTTP request object.
    - view: The view requesting access.

    Methods:
    - has_permission(self, request, view): Checks if the user is authenticated and not Darth Vader.
    """

    def has_permission(self, request, view):
        """
        Checks if the user is authenticated and not Darth Vader.

        This method is called to determine if the user has permission to access the view.
        It denies access if the user is authenticated and has the username 'darthvader'.
        Otherwise, permission is granted.

        Args:
        - request: The HTTP request object.
        - view: The view requesting access.

        Returns:
        - bool: True if the user is authenticated and not Darth Vader, otherwise False.
        """

        if (
            request.user.is_authenticated
            and request.user.username.lower() == "darthvader"
        ):
            raise PermissionDenied(
                "Even the dark side has limits, Darth. You can't publish on Wookiee books!"
            )
        return True
