from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from .models import UserProfile


class HasUserRole(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return self.required_role == UserProfile.ROLE_ADMIN

        try:
            role = request.user.profile.role
        except ObjectDoesNotExist:
            role = UserProfile.ROLE_CUSTOMER

        return role == self.required_role


class IsAdminUser(HasUserRole):
    required_role = UserProfile.ROLE_ADMIN


class IsCustomerUser(HasUserRole):
    required_role = UserProfile.ROLE_CUSTOMER
