from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),

    # Подключаем маршруты из приложения API
    path('api/', include('api.urls')),

    # Доступ к документации Redoc
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]