from rest_framework import serializers
from .models import MockObject


class MockObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockObject
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']