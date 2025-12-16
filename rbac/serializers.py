from rest_framework import serializers
from .models import Resource, Action, Permission, Role, UserRole, AuditLog
from django.contrib.auth import get_user_model

User = get_user_model()


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'endpoint', 'created_at']
        read_only_fields = ['id', 'created_at']


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'name', 'code', 'description']
        read_only_fields = ['id']


class PermissionSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())
    action = serializers.PrimaryKeyRelatedField(queryset=Action.objects.all())

    class Meta:
        model = Permission
        fields = ['id', 'resource', 'action', 'created_at']
        read_only_fields = ['id', 'created_at']


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        required=False
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_email', 'action', 'resource', 'details', 'ip_address', 'user_agent', 'created_at']
        read_only_fields = ['id', 'user', 'user_email', 'ip_address', 'user_agent', 'created_at']

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None