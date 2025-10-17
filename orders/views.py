import requests
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets

from myproject import settings
from .models import Task, Order, Customer
from .serializers import TaskSerializer, OrderSerializer, CustomerSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """List tasks or create a new one."""
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """List tasks or create a new one."""
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


def _api_get(path, params=None):
    """Server-side GET to API with basic error handling."""
    resp = requests.get(f"{settings.API_URL}{path}", params=params, timeout=settings.API_TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def _api_post(path, payload):
    """Server-side POST to API; CSRF is not needed here because it's server-to-server."""
    resp = requests.post(f"{settings.API_URL}{path}", json=payload, timeout=settings.API_TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def orders_list(request):
    """Server-side fetch from DRF to keep keys hidden and avoid CORS."""
    page = request.GET.get("page", "1")
    r = requests.get(f"{settings.API_URL}/orders/?page={page}", timeout=5)
    r.raise_for_status()
    data = r.json()  # expect DRF pagination dict or list
    return render(request, "orders/list.html", {"data": data})

def order_detail(request, pk: int):
    """Fetch single order details from API and render template."""
    r = requests.get(f"{settings.API_URL}/orders/{pk}/", timeout=5)
    r.raise_for_status()
    return render(request, "orders/detail.html", {"order": r.json()})