from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from gallery import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('homepage.urls')),
    path('cards/', include('cards.urls')),

]

handler404 = 'core.views.handler_404'
handler500 = 'core.views.handler_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]