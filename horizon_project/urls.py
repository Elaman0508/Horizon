from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # core — о команде, выезды и т.д.
    path('', include('core.urls')),

    # market — все маршруты для веломаркета
    path('market/', include('market.urls')),
]

# Медиа-файлы (фото велосипедов, выездов)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
