from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serialize Task model for API."""
    class Meta:
        model = Task
        fields = ('id', 'title', 'is_done', 'created_at')
