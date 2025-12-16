from rest_framework import viewsets, permissions
from .models import MockObject
from .serializers import MockObjectSerializer
from rbac.permissions import HasPermission


class MockObjectViewSet(viewsets.ModelViewSet):
    queryset = MockObject.objects.all()
    serializer_class = MockObjectSerializer
    permission_classes = [permissions.IsAuthenticated & HasPermission]
