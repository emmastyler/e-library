from rest_framework import permissions
from .models import UserProfile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Retrieve UserProfile associated with the authenticated user
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return False  # User does not have a UserProfile

        # Check if the user is the owner of the book
        return obj.user_id == user_profile.id


class CanAddBook(permissions.BasePermission):
    """
    Custom permission to allow any user to add a book.
    """
    def has_permission(self, request, view):
        # Allow POST requests (add book)
        return request.method == 'POST'
