from django.contrib.sitemaps import Sitemap
from .models import manga
from django.urls import reverse

class MangaSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return manga.objects.all().order_by('-id')

class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)
