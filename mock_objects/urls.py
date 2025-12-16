from django.urls import path
from .views import MockObjectViewSet

urlpatterns = [
    path('objects/', MockObjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='mock-object-list'),
    path('objects/<int:pk>/', MockObjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='mock-object-detail'),
]