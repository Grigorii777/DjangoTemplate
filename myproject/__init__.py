from .celery import app as celery_app  # expose Celery app for Django import side-effects
__all__ = ('celery_app',)
