from rest_framework import serializers

from .models import Category, Course, Enrollment, Instructor, Lesson, Module, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ("id", "name", "title", "avatar", "bio")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "duration_minutes", "is_preview", "order")


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ("id", "title", "order", "lessons")


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_avatar = serializers.ImageField(source="user.avatar", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user_name", "user_email", "user_avatar", "rating", "comment", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer used for listing / search results."""

    category = CategorySerializer(read_only=True)
    instructor = InstructorSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    effective_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id", "title", "slug", "category", "instructor", "thumbnail",
            "short_description", "level", "language", "price", "discount_price",
            "effective_price", "duration_hours", "students_count",
            "average_rating", "reviews_count", "is_featured", "created_at",
        )


class CourseDetailSerializer(CourseListSerializer):
    """Full serializer with curriculum, reviews, and learning outcomes."""

    modules = ModuleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + (
            "description", "requirements", "what_you_will_learn", "modules", "reviews",
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ("id", "course", "enrolled_at", "progress_percent")
