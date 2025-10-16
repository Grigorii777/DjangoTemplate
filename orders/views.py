from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """List tasks or create a new one."""
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
