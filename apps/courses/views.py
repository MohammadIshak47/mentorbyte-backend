from django.db.models import Avg, Count
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CourseFilter
from .models import Category, Course, Enrollment, Review
from .serializers import (
    CategorySerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    EnrollmentSerializer,
    ReviewSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # return all categories in one shot


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = CourseFilter
    search_fields = ("title", "short_description", "instructor__name", "category__name")
    ordering_fields = ("price", "students_count", "created_at")
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Course.objects
            .filter(is_published=True)
            .select_related("category", "instructor")
            .annotate(
                _avg_rating=Avg("reviews__rating"),
                _reviews_count=Count("reviews"),
            )
        )


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Course.objects
            .filter(is_published=True)
            .select_related("category", "instructor")
            .prefetch_related("modules__lessons", "reviews__user")
        )


class FeaturedCourseListView(generics.ListAPIView):
    """Returns up to 6 featured courses — used by the Home page hero section."""

    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return (
            Course.objects
            .filter(is_published=True, is_featured=True)
            .select_related("category", "instructor")[:6]
        )


class ReviewCreateView(generics.CreateAPIView):
    """POST /api/courses/<slug>/reviews/ — authenticated users only."""

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course = generics.get_object_or_404(Course, slug=self.kwargs["slug"])
        if Review.objects.filter(course=course, user=self.request.user).exists():
            raise ValidationError("You have already reviewed this course.")
        serializer.save(course=course, user=self.request.user)


class EnrollmentListView(generics.ListAPIView):
    """GET /api/enrollments/ — returns courses the current user is enrolled in."""

    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related("course")


class EnrollmentCheckView(APIView):
    """GET /api/courses/<slug>/enrolled/ — returns {enrolled: bool}."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        course = generics.get_object_or_404(Course, slug=slug)
        enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        return Response({"enrolled": enrolled})
