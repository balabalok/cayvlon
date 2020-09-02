from django.db import models
from django.shortcuts import reverse
import urllib.request
from django.core.files import File
import os
from slugify import slugify

class manga(models.Model):
    manga_cover = models.ImageField(upload_to='manga_covers/',blank=True,null=True)
    manga_cover_url = models.CharField(max_length=1024,blank=True,null=True)
    manga_name = models.CharField(max_length=1024)
    manga_other_names = models.CharField(max_length=1024, null=True,blank=True)
    manga_authors = models.CharField(max_length=1024)
    manga_status = models.CharField(max_length=40)
    manga_views = models.PositiveIntegerField(default=0)
    manga_genres = models.TextField()
    manga_descrition = models.TextField()
    manga_slug = models.SlugField(max_length=255,unique=True,blank=False, editable=False)

    def __str__(self):
        return self.manga_name

    def get_absolute_url(self):
        return reverse('minfo', args=[self.manga_slug])

    def get_remote_image(self):
        if self.manga_cover_url and not self.manga_cover:
            result = urllib.request.urlretrieve(self.manga_cover_url)
            self.manga_cover.save(
                os.path.basename(self.manga_cover_url),
                File(open(result[0]))
            )
            self.save()

    def slug(self):
        self.manga_slug = slugify(self.manga_name)

    def save(self, *args, **kwargs):
        self.slug()
        self.get_remote_image()
        super(manga, self).save(*args, **kwargs)

class chapter(models.Model):
    chapter_manga = models.ForeignKey(manga, on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=1024)
    chapter_added = models.DateTimeField(auto_now_add=True)
    chapter_links = models.TextField()
    chapter_slug = models.SlugField(unique=True,blank=False,max_length=255, editable=False)

    def __str__(self):
        return self.chapter_manga.manga_name + ' ' + self.chapter_number

    def slug(self):
        self.chapter_slug = slugify(self.chapter_manga.manga_name +'-chapter-'+self.chapter_number)

    def save(self, *args, **kwargs):

        self.slug()
        super(chapter, self).save(*args, **kwargs)



class genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name
    


    def get_remote_image(self):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
        urllib.request.install_opener(opener)
        if self.image_ch_url and not self.image_ch:
            result = urllib.request.urlretrieve(self.image_ch_url)
            self.image_ch.save(
                os.path.basename(self.image_ch_url),
                File(open(result[0], 'rb'))
            )


            self.save()

class alert(models.Model):
    alert_title = models.CharField(max_length=100)
    alert_data = models.TextField()
    alert_slug = models.SlugField(unique=True)
    alert_date = models.DateTimeField(auto_now_add=True)
    alert_by = models.CharField(max_length=100)
    alert_clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.alert_title

    def slug(self):
        self.alert_slug = slugify(self.alert_title)

    def save(self, *args, **kwargs):
        self.slug()

        super(alert, self).save(*args,**kwargs)