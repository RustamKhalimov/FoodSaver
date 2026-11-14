from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class UserProfile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_CUSTOMER = 'customer'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_CUSTOMER, 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __str__(self):
        return f'{self.user.username} ({self.role})'


def get_user_role(user):
    if user is None or not user.is_authenticated:
        return None

    if user.is_staff or user.is_superuser:
        return UserProfile.ROLE_ADMIN

    try:
        return user.profile.role
    except ObjectDoesNotExist:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': UserProfile.ROLE_CUSTOMER},
        )
        return profile.role
