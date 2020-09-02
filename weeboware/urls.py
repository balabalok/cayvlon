
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from manga.sitemaps import MangaSitemap,StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {'manga': MangaSitemap, 'static': StaticViewSitemap}
from django.views.generic import TemplateView

urlpatterns = [
    path('panell/', admin.site.urls),
    path('', include('manga.urls')),
    path('sitemap.xml',sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', include('robots.urls')),
    path('rate/', include('rateit.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'manga.views.not_found_error'
