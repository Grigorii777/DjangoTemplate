from rest_framework import serializers
from .models import Task, Order, Customer


class TaskSerializer(serializers.ModelSerializer):
    """Serialize Task model for API."""
    class Meta:
        model = Task
        fields = ('id', 'title', 'is_done', 'created_at')

class OrderSerializer(serializers.ModelSerializer):
    """Serialize Task model for API."""
    class Meta:
        model = Order
        fields = "__all__"

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(f"Amount must be positive for {self.__class__.__name__}")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    """Serialize Task model for API."""
    class Meta:
        model = Customer
        fields = "__all__"
