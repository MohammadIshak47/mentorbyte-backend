from django.contrib import admin

from .models import Category, Course, Enrollment, Instructor, Lesson, Module, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "title")


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "instructor", "level", "price", "is_published", "is_featured", "students_count")
    list_filter = ("level", "is_published", "is_featured", "category")
    search_fields = ("title", "instructor__name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    inlines = [LessonInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at", "progress_percent")
