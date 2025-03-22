from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


# Базовый класс для ViewSet, использующих кастомные разрешения
class PermissionViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)


# ViewSet для модели Group (только для чтения)
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# ViewSet для модели Post
class PostViewSet(PermissionViewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination  # Пагинация для постов

    def perform_create(self, serializer):
        """Метод, вызываемый при создании нового поста.
        Автоматически устанавливает текущего пользователя как автора."""
        return serializer.save(author=self.request.user)


# ViewSet для модели Comment
class CommentViewSet(PermissionViewset):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает комментарии, относящиеся к конкретному посту."""
        return self.get_post_obj().comments.all()

    def get_post_obj(self):
        """Получает объект Post по переданному в URL post_pk."""
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_pk')
        )

    def perform_create(self, serializer):
        """Метод, вызываемый при создании комментария.
        Устанавливает автора и пост, к которому относится комментарий."""
        return serializer.save(
            author=self.request.user,
            post=self.get_post_obj()
        )


# ViewSet для модели Follow (подписок)
class FollowViewSet(
    viewsets.GenericViewSet,  # Используется GenericViewSet, т.к. нам нужны только создание и список
    mixins.CreateModelMixin,  # Позволяет создавать подписки
    mixins.ListModelMixin  # Позволяет получать список подписок
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Только для авторизованных пользователей
    filter_backends = (filters.SearchFilter,)  # Включаем возможность поиска по подпискам
    search_fields = ('following__username',)  # Поиск по имени пользователя, на которого подписан

    def get_queryset(self):
        """Возвращает список подписок текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Метод создания подписки, автоматически связывает её с текущим пользователем."""
        serializer.save(user=self.request.user)
