from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """Allows access only to clinic staff/admin users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission: allows access to staff, or to the record's
    owner (e.g. a patient viewing their own appointment/medical record).
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        owner = getattr(obj, "owner", None) or getattr(obj, "patient", None) or getattr(obj, "user", None)
        return owner == request.user


class ReadOnly(permissions.BasePermission):
    """Allows only safe (read-only) HTTP methods."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
