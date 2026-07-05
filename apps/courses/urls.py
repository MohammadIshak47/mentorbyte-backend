from django.urls import path

from .views import (
    CategoryListView,
    CourseDetailView,
    CourseListView,
    EnrollmentCheckView,
    EnrollmentListView,
    FeaturedCourseListView,
    ReviewCreateView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("featured/", FeaturedCourseListView.as_view(), name="featured-courses"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("<slug:slug>/reviews/", ReviewCreateView.as_view(), name="review-create"),
    path("<slug:slug>/enrolled/", EnrollmentCheckView.as_view(), name="enrollment-check"),
    path("my/enrollments/", EnrollmentListView.as_view(), name="my-enrollments"),
]
