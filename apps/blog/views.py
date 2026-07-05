from rest_framework import generics, permissions

from .models import Post, Tag
from .serializers import PostDetailSerializer, PostListSerializer, TagSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ("title", "excerpt", "tags__name")
    ordering_fields = ("created_at", "views")
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).prefetch_related("tags").select_related("author")
        tag_slug = self.request.query_params.get("tag")
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.filter(is_published=True).prefetch_related("tags").select_related("author")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count atomically
        Post.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        return super().retrieve(request, *args, **kwargs)
