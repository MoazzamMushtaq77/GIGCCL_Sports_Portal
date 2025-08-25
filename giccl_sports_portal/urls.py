from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Sports_Users/', include('Sports_Users.urls', namespace='Sports_Users')),
    path('sports_base/', include('sports_base.urls', namespace='sports_base')),
    path('', include('static_pages.urls', namespace='static_pages')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('pwa.urls')),
    # Explicit PWA routes to avoid conflicts
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/javascript'), name='serviceworker'),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    path('offline/', TemplateView.as_view(template_name='static_pages/offline.html'), name='offline'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)