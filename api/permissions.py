from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем аккаунта.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь создателем оценки.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsStaffUser(permissions.BasePermission):
    """
    Проверяет, является ли пользователь администратором (is_staff).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
