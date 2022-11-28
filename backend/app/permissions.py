from rest_framework import permissions


class AuthorIsRequestUserPermission(permissions.BasePermission):
    '''Делаем так, чтобы изменять и добавлять объекты
       мог только их автор'''

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
