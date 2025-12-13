from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = "You must be the owner of this object to perform this action."    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
    
class IsVerifiedAndInfluencer(permissions.BasePermission):
    message = "You must be a verified influencer to perform this action."    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_influencer and request.user.is_verified
    
class IsOwnerOrAdmin(permissions.BasePermission):
    message = "You must be the owner or an admin to perform this action."
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.creator == request.user