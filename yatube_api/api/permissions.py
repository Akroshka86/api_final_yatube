from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем.
    Создание — только авторизованным пользователям.
    Изменение и удаление — только автору объекта.
    """

    def has_permission(self, request, view):
        # Разрешаем чтение всем, а остальные методы только аутентифицированным пользователям
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Чтение доступно всем, изменения — только автору
        return request.method in permissions.SAFE_METHODS or obj.author == request.user