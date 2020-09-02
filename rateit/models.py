from django.db import models

from manga.models import manga

class rate(models.Model):

    rate_manga = models.ForeignKey(manga, on_delete=models.PROTECT)
    hearts = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return self.rate_manga.manga_name

class ip_rate(models.Model):

    connection = models.ForeignKey(rate, on_delete=models.PROTECT)
    ip_of_rater = models.CharField(max_length=30)

    def __str__(self):
        return self.ip_of_rater


