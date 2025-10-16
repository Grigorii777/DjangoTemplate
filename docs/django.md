# Django Start
### Installation
```bash
pip install --upgrade pip
pip install django djangorestframework
```

### Project creation
```bash
django-admin startproject myproject .
```

### App creation
```bash
python manage.py startapp orders
```

### Connecting the application and DRF myproject/settings.py → add:
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',  # DRF
    'orders',          # our app
]
```

### The simplest model orders/models.py
```python
from django.db import models

class Task(models.Model):
    """Minimal task model for demo."""
    title = models.CharField(max_length=200)   # short title
    is_done = models.BooleanField(default=False)  # completion flag
    created_at = models.DateTimeField(auto_now_add=True)  # audit field

    def __str__(self) -> str:  # type hint for IDE
        return self.title

```

### Serialiser and view (if you use DRF) orders/serializers.py
```bash
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serialize Task model for API."""
    class Meta:
        model = Task
        fields = ('id', 'title', 'is_done', 'created_at')

```

### orders/views.py
```bash
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """List tasks or create a new one."""
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
```

### Routes orders/urls.py
```bash
from django.urls import path
from .views import TaskListCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # basic CRUD (list/create)
]
```

### myproject/urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),  # mount app API
]
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Launch
```bash
python manage.py runserver
```

### Test 
```bash
# GET: should return [] when the database is empty
curl -s http://127.0.0.1:8000/api/tasks/

# POST: create record (DRF)
curl -s -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"First task"}'

# Repeat GET: must return the created task
curl -s http://127.0.0.1:8000/api/tasks/
```

### Check
```bash
http://127.0.0.1:8000/api/tasks/
```

```bash
http://127.0.0.1:8000/admin/
```