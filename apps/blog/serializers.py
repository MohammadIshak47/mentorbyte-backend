from rest_framework import serializers

from .models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class PostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_avatar = serializers.ImageField(source="author.avatar", read_only=True)
    read_time_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id", "title", "slug", "cover_image", "excerpt",
            "author_name", "author_avatar", "tags",
            "read_time_minutes", "views", "created_at",
        )


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ("content",)
