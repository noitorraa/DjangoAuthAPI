from django.urls import path
from .views import ResourceViewSet, ActionViewSet, PermissionViewSet, RoleViewSet, UserRoleViewSet, AuditLogViewSet

urlpatterns = [
    # Resources
    path('resources/', ResourceViewSet.as_view({'get': 'list', 'post': 'create'}), name='resource-list'),
    path('resources/<int:pk>/', ResourceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='resource-detail'),
    
    # Actions
    path('actions/', ActionViewSet.as_view({'get': 'list', 'post': 'create'}), name='action-list'),
    path('actions/<int:pk>/', ActionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='action-detail'),
    
    # Permissions
    path('permissions/', PermissionViewSet.as_view({'get': 'list', 'post': 'create'}), name='permission-list'),
    path('permissions/<int:pk>/', PermissionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='permission-detail'),
    
    # Roles
    path('roles/', RoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='role-list'),
    path('roles/<int:pk>/', RoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='role-detail'),
    
    # User Roles
    path('user-roles/', UserRoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-role-list'),
    path('user-roles/<int:pk>/', UserRoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-role-detail'),
    
    # Audit Logs
    path('audit-logs/', AuditLogViewSet.as_view({'get': 'list'}), name='audit-log-list'),
    path('audit-logs/<int:pk>/', AuditLogViewSet.as_view({'get': 'retrieve'}), name='audit-log-detail'),
]