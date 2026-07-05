"""
Order creation and checkout.

This project does NOT integrate a live payment gateway. Stripe is not
available for account creation in every country (including Bangladesh),
so rather than block the whole checkout flow on a gateway that may be
unreachable, purchases are confirmed instantly on the backend:

1. POST /api/orders/checkout/  — validates the course(s), creates an Order
   marked PAID immediately, creates the matching Enrollment records, and
   clears the user's cart.
2. The frontend then redirects straight to a payment-success page.

This still exercises the full order / enrollment data model — which is
what matters for a portfolio project — without depending on any
third-party payment provider. If you later want a real gateway, this is
the single place to plug one in (e.g. SSLCommerz, bKash, or Stripe from
a supported country) — see the inline note in CheckoutView.
"""
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.courses.models import Course, Enrollment

from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutView(APIView):
    """
    POST /api/orders/checkout/
    Body: { "course_id": "<uuid>" } for a single "Buy Now" purchase, OR
          an empty body to check out everything currently in the cart.

    Returns the created Order (already marked PAID) plus the courses the
    user is now enrolled in.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if course_id:
            # Single-course "Buy Now"
            try:
                course = Course.objects.get(pk=course_id, is_published=True)
            except Course.DoesNotExist:
                return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
            courses_to_buy = [course]
        else:
            # Full cart checkout
            try:
                cart = user.cart
            except Cart.DoesNotExist:
                return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
            cart_items = cart.items.select_related("course").all()
            if not cart_items.exists():
                return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
            courses_to_buy = [item.course for item in cart_items]

        # Skip courses the user already owns
        already_enrolled = set(
            Enrollment.objects.filter(user=user, course__in=courses_to_buy)
            .values_list("course_id", flat=True)
        )
        courses_to_buy = [c for c in courses_to_buy if c.id not in already_enrolled]

        if not courses_to_buy:
            return Response(
                {"detail": "You are already enrolled in all selected courses."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = sum(c.effective_price for c in courses_to_buy)

        # ------------------------------------------------------------------
        # Create the order and immediately mark it PAID.
        #
        # To plug in a real gateway later: create the Order as PENDING here,
        # redirect the user to the gateway's hosted checkout page, and move
        # the "mark PAID + create Enrollment" logic below into that
        # gateway's webhook/callback handler instead.
        # ------------------------------------------------------------------
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                status=Order.Status.PAID,
                total_amount=total_amount,
                paid_at=timezone.now(),
            )
            for course in courses_to_buy:
                OrderItem.objects.create(
                    order=order,
                    course=course,
                    course_title=course.title,
                    price=course.effective_price,
                )
                Enrollment.objects.get_or_create(user=user, course=course)
                course.students_count = course.enrollments.count()
                course.save(update_fields=["students_count"])

            # Clear the cart if this was a cart checkout
            if not course_id:
                user.cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """GET /api/orders/ — the current user's order history."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
