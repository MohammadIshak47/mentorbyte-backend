import django_filters

from .models import Course


class CourseFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    level = django_filters.CharFilter(lookup_expr="iexact")
    language = django_filters.CharFilter(lookup_expr="icontains")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Course
        fields = ("category", "level", "language", "min_price", "max_price", "is_featured")
