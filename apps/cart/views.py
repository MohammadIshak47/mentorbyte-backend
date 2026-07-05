from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course

from .models import Cart, CartItem
from .serializers import CartSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    """GET  /api/cart/     — retrieve the user's cart
       POST /api/cart/     — add a course to the cart
       DELETE /api/cart/   — clear the entire cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"detail": "course_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id, is_published=True)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        cart = get_or_create_cart(request.user)

        if CartItem.objects.filter(cart=cart, course=course).exists():
            return Response({"detail": "Course is already in your cart."}, status=status.HTTP_400_BAD_REQUEST)

        CartItem.objects.create(cart=cart, course=course, price=course.effective_price)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)


class CartItemDeleteView(APIView):
    """DELETE /api/cart/<item_id>/ — remove a single item from the cart."""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        cart = get_or_create_cart(request.user)
        try:
            item = cart.items.get(pk=item_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(CartSerializer(cart).data)
