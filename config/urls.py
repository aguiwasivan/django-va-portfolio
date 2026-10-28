from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from core.sitemaps import PageSitemap, ProjectSitemap
urlpatterns = [path(settings.ADMIN_URL,admin.site.urls),path('',include('core.urls')),path('projects/',include('projects.urls')),path('sitemap.xml',sitemap,{'sitemaps':{'pages':PageSitemap,'projects':ProjectSitemap}},name='sitemap')]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
