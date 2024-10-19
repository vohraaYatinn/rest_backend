# permissions.py
import jwt
from rest_framework.permissions import BasePermission

class IsUserAuth(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        token = request.headers.get("jwtToken")
        if not token:
            return False
        decoded_token = jwt.decode(token,"secretKeyRight34", algorithms=['HS256'])
        if decoded_token:
            request.user.id = decoded_token.get("user")
            return True
        else:
            return False

class IsAdminAuth(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        token = request.headers.get("jwtToken")
        if not token:
            return False
        decoded_token = jwt.decode(token, "secretKeyRight34", algorithms=['HS256'])
        if decoded_token:
            request.user.phone = decoded_token.get("user")
            return True
        else:
            return False