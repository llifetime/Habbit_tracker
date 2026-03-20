from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только владельцу объекта.
    Для публичных привычек - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешены безопасные методы (GET, HEAD, OPTIONS) для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для остальных методов проверяем, является ли пользователь владельцем
        return obj.owner == request.user
