from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'You are not permitted to update this'
    def has_object_permissions(self, request, view, obj):
        return obj.user == request.user