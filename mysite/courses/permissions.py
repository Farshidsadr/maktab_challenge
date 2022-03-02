from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsCourseTeacherOrReadOnly(permissions.BasePermission):
    """
    Allow access to readonly requests, and for other requests i.e. update, only related course teacher or super admin
    get access to perform action.
    """
    def has_object_permission(self, request, view, obj):
        # Because I did not know about your policies, I considered readonly methods can accessible for all request even
        # unauthenticated requests
        return bool(
            request.method in SAFE_METHODS or
            obj.teacher.user == request.user or
            request.user.is_superuser
        )


class IsCourseTeacher(permissions.BasePermission):
    """
    Allow access to mutable actions only for course's related teacher
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.teacher.user == request.user
        )
