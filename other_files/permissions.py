from rest_framework import permissions
from rolepermissions.checkers import has_role
from rolepermissions.roles import get_user_roles


class IsCandidate(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return has_role(user,"candidate")


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return has_role(user,"employer")
