from django.db import models

class Task(models.Model):
    """Minimal task model for demo."""
    title = models.CharField(max_length=200)   # short title
    is_done = models.BooleanField(default=False)  # completion flag
    created_at = models.DateTimeField(auto_now_add=True)  # audit field

    def __str__(self) -> str:  # type hint for IDE
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:  # type hint for IDE
        return self.name


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

    def __str__(self) -> str:  # type hint for IDE
        return self.title

