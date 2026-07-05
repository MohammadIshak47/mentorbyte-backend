from rest_framework import serializers

from apps.courses.serializers import CourseListSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "course", "course_id", "price", "added_at")
        read_only_fields = ("id", "price", "added_at")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    items_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items", "total_price", "items_count", "updated_at")
