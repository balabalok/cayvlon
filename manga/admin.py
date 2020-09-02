from django.contrib import admin
from .models import manga,chapter,genre,alert

class MangaSearch(admin.ModelAdmin):
    search_fields = ['manga_name']

class ChapterSearch(admin.ModelAdmin):
    search_fields = ['chapter_manga__manga_name']

admin.site.register(manga,MangaSearch)
admin.site.register(chapter, ChapterSearch)
admin.site.register(genre)
admin.site.register(alert)
