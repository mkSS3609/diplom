from rest_framework import serializers

from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Отсутствует текст!')
        return value


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(use_url=True, required=False)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ['id','author', 'text', 'image', 'created_at', 'likes_count', 'comments']
        read_only_fields = ['id', 'created_at', 'likes_count', 'comments']

    def validate(self, value):
        request = self.context.get('request')
        if request and not request.user.is_authenticated:
            raise serializers.ValidationError('Требуется аутентификация')
        return value


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image']
        read_only_fields = ['id']

    def validate_text(self, value):
        if not value.strip() or not self.initial_data.get('image'):
            raise serializers.ValidationError('Отсутствует текст и/или изображение!')
        return value