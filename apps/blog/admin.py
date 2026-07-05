from django.contrib import admin

from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "views", "created_at")
    list_filter = ("is_published", "tags")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
