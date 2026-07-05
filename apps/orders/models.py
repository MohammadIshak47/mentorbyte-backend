import uuid

from django.conf import settings
from django.db import models

from apps.courses.models import Course


class Order(models.Model):
    class Status(models.TextChoices):
        PAID = "paid", "Paid"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PAID)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} — {self.user.email} — {self.status}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    course_title = models.CharField(max_length=200)  # snapshot, survives course deletion
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} — {self.course_title}"
