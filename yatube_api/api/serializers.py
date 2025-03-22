from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Group, Follow

# Сериализатор для модели Post
class PostSerializer(serializers.ModelSerializer):
    # Поле author представлено в виде username и доступно только для чтения
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'  # Включает все поля модели


# Сериализатор для модели Comment
class CommentSerializer(serializers.ModelSerializer):
    # Автор комментария отображается как username и не изменяется пользователем
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'  # Включает все поля модели
        read_only_fields = ('post',)  # Поле post нельзя изменять после создания


# Сериализатор для модели Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')  # Явно указываем нужные поля
        read_only_fields = ('id', 'title', 'slug', 'description')  # Все поля только для чтения


# Сериализатор для модели Follow (подписки)
class FollowSerializer(serializers.ModelSerializer):
    # user — текущий пользователь (по умолчанию)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault()
    )
    # following — пользователь, на которого подписываются
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')  # Указываем только нужные поля
        validators = (
            # Проверка уникальности подписки (нельзя подписаться дважды)
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка уже существует'
            ),
        )

    # Дополнительная валидация: нельзя подписаться на самого себя
    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Попытка подписаться на себя же'
            )
        return data
