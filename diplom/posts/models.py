from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    text = models.TextField(max_length=2000, blank=True) # убрать null
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'Пост {self.id} от {self.author.username}'

    def likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Комментарий от {self.author.username} на пост {self.post.id}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['post', 'user']
        indexes = [models.Index(fields=['post', 'user'])]

    def __str__(self):
        return f'{self.user.username} лайкнул пост {self.post.id}'