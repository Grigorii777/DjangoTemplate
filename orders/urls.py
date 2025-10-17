from django.urls import path
from .views import TaskListCreateView, OrderViewSet, CustomerViewSet

# 2 types
# without delete put and id tasks
# http://127.0.0.1:8000/api/tasks/
extra_urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # basic CRUD (list/create)
]

# with delete put and id order
# http://127.0.0.1:8000/api/orders/
# http://127.0.0.1:8000/api/orders/3
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r"customers", CustomerViewSet, basename='customer')

urlpatterns = router.urls + extra_urlpatterns
