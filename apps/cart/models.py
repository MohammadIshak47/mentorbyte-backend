import uuid

from django.conf import settings
from django.db import models

from apps.courses.models import Course


class Cart(models.Model):
    """One cart per user — a persistent shopping session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user.email})"

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    @property
    def items_count(self):
        return self.items.count()


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Snapshot the price at the time of adding so it doesn't change under the user
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added_at"]
        constraints = [
            models.UniqueConstraint(fields=["cart", "course"], name="unique_course_in_cart"),
        ]

    def __str__(self):
        return f"{self.cart.user.email} — {self.course.title}"
