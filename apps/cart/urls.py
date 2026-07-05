from django.urls import path

from .views import CartItemDeleteView, CartView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("<uuid:item_id>/", CartItemDeleteView.as_view(), name="cart-item-delete"),
]
