# Marat/urls.py — ФИНАЛЬНАЯ ВЕРСИЯ
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from blog.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  
    path('', include('django.contrib.auth.urls')),  
    path('register/', register, name='register'),
]

urlpatterns += i18n_patterns(
    path('', include('blog.urls')),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)