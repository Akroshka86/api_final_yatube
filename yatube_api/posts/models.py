from django.contrib.auth import get_user_model
from django.db import models

# Получаем модель пользователя
User = get_user_model()

# Модель группы (сообщество)
class Group(models.Model):
    title = models.CharField(max_length=200)  # Название группы
    slug = models.SlugField(max_length=50, unique=True)  # Уникальный идентификатор в URL
    description = models.TextField()  # Описание группы

    def __str__(self):
        return self.title  # Отображение названия группы в админке


# Модель поста (записи)
class Post(models.Model):
    text = models.TextField()  # Текст поста
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)  # Дата создания
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )  # Автор поста
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )  # Опциональное изображение
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='posts',
        null=True, blank=True
    )  # Группа, к которой относится пост (необязательное поле)

    class Meta:
        ordering = ['-pub_date']  # Сортировка постов по дате (от новых к старым)

    def __str__(self):
        return self.text[:20]  # Отображаем первые 20 символов текста в админке


# Модель комментария к посту
class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )  # Автор комментария
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )  # Связанный пост
    text = models.TextField()  # Текст комментария
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )  # Дата создания (оптимизирована для поиска)

    def __str__(self):
        return f'Комментарий от {self.author} к посту {self.post}'


# Модель подписки на авторов
class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )  # Кто подписался
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )  # На кого подписались

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),  # Запрещаем дублирующиеся подписки
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            ),  # Запрещаем подписку на самого себя
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
