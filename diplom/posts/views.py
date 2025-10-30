from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment, Like
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer


# Create your views here.

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied(detail='Требуется аутентификация')
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'status': 'unliked', 'likes_count': post.likes_count()}, status=status.HTTP_200_OK)
        return Response({'status': 'liked', 'likes_count': post.likes_count()}, status=status.HTTP_201_CREATED)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).select_related('author')

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied(detail='Требуется аутентификация')
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)