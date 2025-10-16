from time import sleep

from celery import shared_task

@shared_task(bind=True, max_retries=3)
def process_task(self, task_id: int) -> str:
    """Dummy async processing."""
    sleep(10)
    return f"Processed task {task_id}"
