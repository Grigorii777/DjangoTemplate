# Celery Start
```bash
pip install 'celery[redis]'
```

### myproject/celery.py
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')               # create Celery app
app.config_from_object('django.conf:settings', namespace='CELERY')  # read CELERY_* from settings
app.autodiscover_tasks()                # auto-load tasks.py in apps
```

### myproject/__init__.py
```bash
from .celery import app as celery_app  # expose Celery app for Django import side-effects
__all__ = ('celery_app',)
```

### orders/tasks.py
```python
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def process_task(self, task_id: int) -> str:
    """Dummy async processing."""
    # TODO: add real processing logic here
    return f"Processed task {task_id}"
```

### Run
```bash
celery -A myproject worker -l info
```

# Django Celery check
```bash
python manage.py shell
```

```python
from orders.tasks import process_task
from celery.result import AsyncResult
result = process_task.delay(42)
res = AsyncResult(result.id)
print(res.status)      # SUCCESS / PENDING / RETRY / FAILURE
print(res.result)      # Processed task 42
```
