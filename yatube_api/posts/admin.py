from django.contrib import admin
from .models import Post, Group, Comment, Follow

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'pub_date', 'author', 'group')
    list_filter = ('pub_date', 'author', 'group')
    search_fields = ('text',)
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'text', 'created')
    list_filter = ('created', 'author')
    search_fields = ('text',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')
    list_filter = ('user', 'following')
    search_fields = ('user__username', 'following__username')