from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import AbstractUser
from django.db import models

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class User(AbstractUser):
    # users this user follows
    following = models.ManyToManyField(
        "self",
        through="Follow",
        related_name="followers",
        symmetrical=False,
    )

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following_rel", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="follower_rel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        indexes = [
            models.Index(fields=["follower", "following"])
        ]

    def __str__(self):
        return f"{self.follower} -> {self.following}"
    
    class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        # if custom UserModel has .following (ManyToMany)
        following_qs = user.following.all()
        # Include user's own posts? optionally add `| User.objects.filter(pk=user.pk)` if you want own posts
        return ollowing_qs).select_related('author').order_by('-created_at')Post.objects.filter(author__in=following_users).order_by