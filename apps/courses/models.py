import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to="instructors/", blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="courses")
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name="courses")
    thumbnail = models.ImageField(upload_to="courses/thumbnails/", blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    language = models.CharField(max_length=50, default="English")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    duration_hours = models.PositiveIntegerField(default=0, help_text="Total course length in hours")
    requirements = models.JSONField(default=list, blank=True, help_text="List of prerequisite strings")
    what_you_will_learn = models.JSONField(default=list, blank=True, help_text="List of learning outcome strings")
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    students_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["is_published", "is_featured"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price is not None else self.price

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(avg=models.Avg("rating"))
        return round(agg["avg"] or 0, 1)

    @property
    def reviews_count(self):
        return self.reviews.count()


class Module(models.Model):
    """A section/chapter within a course's curriculum."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False, help_text="Can be watched without purchase")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["course", "user"], name="one_review_per_user_per_course"),
        ]

    def __str__(self):
        return f"{self.user.email} → {self.course.title} ({self.rating}/5)"


class Enrollment(models.Model):
    """Created once an order for a course is paid."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress_percent = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="one_enrollment_per_user_per_course"),
        ]

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"
