from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend_hub import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users_app.api.urls')),
    path('api/videos/', include('videos_app.api.urls')),
] + staticfiles_urlpatterns()

# ✅ WICHTIG: Nur im Development (wenn DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
