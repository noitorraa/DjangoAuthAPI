from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from .models import Resource, Action, Permission, Role, UserRole, AuditLog
from .serializers import (
    ResourceSerializer,
    ActionSerializer,
    PermissionSerializer,
    RoleSerializer,
    UserRoleSerializer,
    AuditLogSerializer
)
from .permissions import HasPermission
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def perform_create(self, serializer):
        serializer.save()
        self._log_action("create", "resource", serializer.data)

    def perform_update(self, serializer):
        self._log_action("update", "resource", serializer.data)

    def perform_destroy(self, instance):
        self._log_action("delete", "resource", {"id": instance.id, "name": instance.name})


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def perform_create(self, serializer):
        serializer.save()
        self._log_action("create", "action", serializer.data)

    def perform_update(self, serializer):
        self._log_action("update", "action", serializer.data)

    def perform_destroy(self, instance):
        self._log_action("delete", "action", {"id": instance.id, "name": instance.name})


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def perform_create(self, serializer):
        serializer.save()
        self._log_action("create", "permission", serializer.data)

    def perform_update(self, serializer):
        self._log_action("update", "permission", serializer.data)

    def perform_destroy(self, instance):
        self._log_action("delete", "permission", {"id": instance.id})


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def perform_create(self, serializer):
        serializer.save()
        self._log_action("create", "role", serializer.data)

    def perform_update(self, serializer):
        self._log_action("update", "role", serializer.data)

    def perform_destroy(self, instance):
        self._log_action("delete", "role", {"id": instance.id, "name": instance.name})


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserRole.objects.all()
        return UserRole.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
        self._log_action("create", "user_role", serializer.data)

    def perform_update(self, serializer):
        self._log_action("update", "user_role", serializer.data)

    def perform_destroy(self, instance):
        self._log_action("delete", "user_role", {"id": instance.id})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AuditLog.objects.all()
        return AuditLog.objects.filter(user=self.request.user)


class BaseViewSet:
    """Базовый класс для логирования действий"""
    
    def _log_action(self, action, resource, details):
        """Логирование действий администратора"""
        ip_address = self._get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def _get_client_ip(self):
        """Получение IP адреса клиента"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
