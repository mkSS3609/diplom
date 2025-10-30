from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:pk>/liked/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
] + router.urls

