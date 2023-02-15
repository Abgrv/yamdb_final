from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Права доступа администратор"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return False


class IsAdminOrReadOnly(BasePermission):
    """Права доступа администратор или только для чтения"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsReadOnlyOrIsAuthorOrIsModerator(BasePermission):
    """Права доступа администратор, модератор, автор или только для чтения"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user)
