from django.shortcuts import render,redirect
from django.http import Http404
from .models import rate,ip_rate
from manga.models import manga
from django.db.models import F
from django.db import connection


def rate_(request):
    if request.method == 'POST':
        if rate.objects.filter(rate_manga__manga_slug=request.POST['manga']).exists():
            # Update
            manga_object = manga.objects.get(manga_slug=request.POST['manga'])
            rate.objects.filter(rate_manga=manga_object).update(hearts=F('hearts') + 1)

            # Add ip
            ip_rate_new = ip_rate()
            ip_rate_new.connection = rate.objects.get(rate_manga=manga_object)
            ip_rate_new.ip_of_rater = request.POST['ip']
            ip_rate_new.save()
        else:
            # New object
            new_manga_rate = rate()
            new_manga_rate.rate_manga = manga.objects.get(manga_slug=request.POST['manga'])
            new_manga_rate.save()

            #Update
            manga_object = manga.objects.get(manga_slug=request.POST['manga'])
            rate.objects.filter(rate_manga=manga_object).update(hearts=F('hearts') + 1)

            # Add ip
            ip_rate_new = ip_rate()
            ip_rate_new.connection = rate.objects.get(rate_manga=manga_object)
            ip_rate_new.ip_of_rater = request.POST['ip']
            ip_rate_new.save()

        connection.close()


        return redirect('minfo', m_slug=request.POST['manga'])

    else:
        return Http404