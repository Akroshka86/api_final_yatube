from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

# Создаём роутер для автоматической генерации маршрутов
router = DefaultRouter()
# Регистрируем маршруты для постов
router.register(r'posts', PostViewSet, basename='posts')
# Регистрируем маршруты для групп
router.register(r'groups', GroupViewSet, basename='groups')
# Регистрируем маршруты для подписок (follow)
router.register('follow', FollowViewSet, basename='followers')
# Регистрируем маршруты для комментариев к постам
router.register(
    r'^posts/(?P<post_pk>\d+)/comments',  # URL-адрес с параметром post_pk
    CommentViewSet,
    basename='comments'
)

# Основные маршруты API
urlpatterns = [
    path('v1/', include(router.urls)),  # Подключаем маршруты, созданные роутером
    path('v1/', include('djoser.urls')),  # Djoser - обработка пользователей (регистрация, сброс пароля и т. д.)
    path('v1/', include('djoser.urls.jwt')),  # Подключение JWT-аутентификации для пользователей
]