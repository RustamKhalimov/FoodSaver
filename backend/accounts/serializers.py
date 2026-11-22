from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile, get_user_role


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
        )
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': UserProfile.ROLE_CUSTOMER},
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    notifications_enabled = serializers.BooleanField(
        source='profile.notifications_enabled',
        required=False,
    )
    reminder_time = serializers.TimeField(
        source='profile.reminder_time',
        format='%H:%M',
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'notifications_enabled',
            'reminder_time',
        ]
        read_only_fields = ['id', 'username', 'role']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = super().update(instance, validated_data)

        if profile_data:
            profile = user.profile
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save(update_fields=[*profile_data.keys()])

        return user

    def get_role(self, obj):
        return get_user_role(obj) or UserProfile.ROLE_CUSTOMER
