from django.urls import path
from .views import PostViewSet, CommentViewSet

urlpatterns = [
    path(
        'posts/',
        PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'
    ),
    path(
        'posts/<int:pk>/',
        PostViewSet.as_view({'get': 'retrieve', 'post': 'partial_update', 'delete': 'destroy'}), name='post-detail'
    ),
    path(
        'posts/<int:post_id>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'
    ),
    path(
        'posts/<int:pk>/liked/',
        PostViewSet.as_view({'post': 'like'}), name='post-like'
    ),
]

