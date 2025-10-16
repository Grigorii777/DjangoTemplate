# Django ORM

### orders/models.py
```python
from django.db import models

class Order(models.Model):
    """Simple order model for ORM practice."""
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

```bash
python manage.py makemigrations
python manage.py migrate
```

### CRUD operations in shell
```bash
python manage.py shell
```

```python
from orders.models import Order
order = Order.objects.create(title="Sausage batch #1", amount=120.50)
```

### Read
```bash
Order.objects.all()                     
Order.objects.filter(is_paid=False)     
Order.objects.get(id=1)                 
Order.objects.filter(amount__gt=100)   
Order.objects.first()
Order.objects.last()
Order.objects.exclude(is_paid=True)
```

### Update
```bash
from orders.models import Order
order = Order.objects.get(id=1)
order.is_paid = True
order.save()
# or:
Order.objects.filter(id=1).update(is_paid=True)

```

### Delete
```bash
Order.objects.filter(is_paid=False).delete()
```

### Abstracts and aggregates
```python
from orders.models import Order
from django.db.models import Count, Sum, Avg

Order.objects.aggregate(total_sum=Sum("amount"))
# {'total_sum': Decimal('841')}
Order.objects.values("is_paid").annotate(total=Count("id"))
# <QuerySet [{'is_paid': False, 'total': 4}, {'is_paid': True, 'total': 1}]>
```

### Lookup expressions (filters with suffixes)
```python
from orders.models import Order
# contains / icontains — search by substring
Order.objects.filter(title__icontains="sausage")
Order.objects.filter(amount__range=(50, 150))
Order.objects.filter(created_at__date__gte="2025-01-01")
Order.objects.filter(delivery_info__isnull=False)
```

### Connections
```python
from django.db import models
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class DeliveryInfo(models.Model):
    """One-to-One relationship: each order has one delivery info record."""
    address = models.CharField(max_length=255)
    delivery_date = models.DateField(null=True, blank=True)

class Tag(models.Model):
    """Represents a tag that can be assigned to many orders."""
    name = models.CharField(max_length=50, unique=True)

class Order(models.Model):
    """Simple order model for ORM practice."""
    # One-to-Many
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )
    """
    CASCADE — deletes related objects.
    PROTECT — prohibits deletion of a parent if there are children (throws ProtectedError).
    RESTRICT — Similarly prohibits, but without reverse deletion; closer to SQL RESTRICT.
    SET_NULL — sets NULL in FK (null=True is required).
    SET_DEFAULT — sets the default value (you need default=...).
    DO_NOTHING — does nothing (may compromise integrity, use with CAUTION!!!).
    """

    # One-to-One
    delivery_info = models.OneToOneField(
        DeliveryInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order",
    )

    # Many-to-Many
    tags = models.ManyToManyField(
        Tag,
        related_name="orders",
        blank=True,
    )
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

```

```bash
python manage.py makemigrations
python manage.py migrate
```

```python
from orders.models import Customer, Order
c = Customer.objects.create(name="Grisha")
Order.objects.create(customer=c, title="Batch #2", amount=200)
c.orders.all() 
```

### Working with relationships (ForeignKey, OneToOne, ManyToMany)
```python
from orders.models import Customer, Order
Order.objects.filter(customer__name="Grisha")
Customer.objects.get(name="Grisha").orders.all()
```

# Query optimisation
### select_related() 
#### Used for ForeignKey and OneToOne (JOIN — one SQL string):
#### Without this, Django would make one request for each connection (N+1 problem).
```python
from orders.models import Order
orders = Order.objects.select_related("customer", "delivery_info").all()
for o in orders:
    print(o.customer.name, o.delivery_info.address)
```

### prefetch_related()
#### Used for ManyToMany and reverse ForeignKeys.
#### Django makes two requests (main + for communication) and combines the results in Python.
```python
from orders.models import Order
orders = Order.objects.prefetch_related("tags").all()
for o in orders:
    print(o.title, [t.name for t in o.tags.all()])
```

### F и Q expressions
```python
from orders.models import Order
from django.db.models import F
Order.objects.update(amount=F("amount") * 1.1)
```

### Q — complex conditions (OR / AND / NOT)
```python
from django.db.models import Q
from orders.models import Order
Order.objects.filter(Q(is_paid=True) | Q(amount__gt=500))
Order.objects.filter(~Q(is_paid=True))  # NOT
```

### Values / ValuesList (for selecting dictionaries)
```python
from orders.models import Order
Order.objects.values("title", "amount")  # -> list[dict]
Order.objects.values_list("title", "amount")  # -> list[tuple]
Order.objects.values_list("id", flat=True)  # -> list[id]
```

### Related subqueries (Subquery / OuterRef)
```python
from django.db.models import OuterRef, Subquery
from orders.models import Order, Customer
latest_orders = Order.objects.filter(customer=OuterRef("pk")).order_by("-created_at")
Customer.objects.annotate(last_order=Subquery(latest_orders.values("title")[:1]))
```

### Exists (to check for the existence of a subquery)
```python
from django.db.models import Exists, OuterRef
from orders.models import Order, Customer
paid_orders = Order.objects.filter(is_paid=True, customer=OuterRef("pk"))
Customer.objects.annotate(has_paid_orders=Exists(paid_orders))
```

### RAW query
```python
from orders.models import Order
Order.objects.raw("SELECT id, title, amount FROM orders_order WHERE amount > %s", [100])
```

## Transactions
### transaction.atomic() supports nested blocks — savepoints are created.
```python
from django.db import transaction
from orders.models import Order, Customer

with transaction.atomic():
    customer = Customer.objects.create(name="Grisha")
    Order.objects.create(customer=customer, title="Batch #42", amount=100)
```

### Row locking For competitive scenarios — select_for_update().
### blocks the row until the end of the transaction (works in PostgreSQL, MySQL).
```bash
from django.db import transaction

with transaction.atomic():
    order = Order.objects.select_for_update().get(id=1)
    order.amount += 10
    order.save()
```

### Setting the isolation level In settings.py, you can specify:
```txt
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'isolation_level': 'repeatable read',
        },
    }
}
```

### 
```bash

```
