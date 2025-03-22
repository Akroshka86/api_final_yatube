from django.contrib import admin
from .models import Post, Group, Comment, Follow

# Админка для модели Group
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')   # Поля, отображаемые в списке
    search_fields = ('title',)                              # Поиск по названию группы
    prepopulated_fields = {"slug": ("title",)}              # Автоматически заполняет slug на основе title

# Админка для модели Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'pub_date', 'author', 'group')    # Отображаемые поля
    list_filter = ('pub_date', 'author', 'group')                   # Фильтрация по дате, автору и группе
    search_fields = ('text',)                                       # Поиск по тексту поста
    raw_id_fields = ('author',)                                     # Улучшает выбор автора при большом количестве пользователей
    date_hierarchy = 'pub_date'                                     # Позволяет удобно фильтровать по дате публикации

# Админка для модели Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'text', 'created')      # Поля в списке
    list_filter = ('created', 'author')                             # Фильтрация по дате создания и автору
    search_fields = ('text',)                                       # Поиск по тексту комментария

# Админка для модели Follow (подписки)
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')                      # Поля, отображаемые в списке
    list_filter = ('user', 'following')                             # Фильтрация по пользователю и подпискам
    search_fields = ('user__username', 'following__username')       # Поиск по имени пользователей
