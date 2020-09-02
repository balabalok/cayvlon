from rateit.models import rate,ip_rate
from django.shortcuts import render,get_object_or_404
from .models import manga,chapter,genre,alert
from django.core.paginator import Paginator
from django.db.models import F,Max,Q
from ipware import get_client_ip
from django.db import connection
import requests
import random


def home_2(request):
    template = 'home/home_2.html'

    # Most Clicked
    manga_most_clicked = manga.objects.all().order_by('-manga_views')[0:12]

    # Latest Updated
    manga_updated = manga.objects.annotate(
        last_update_time=Max('chapter__chapter_added')
    ).order_by('-last_update_time')[0:48]

    # Just Added
    manga_new = manga.objects.all().order_by('-id')[0:6]

    # Random

    students = manga.objects.all()
    for i in range(500):
        mangax = random.choice(students)






    context = {
        'top_manga':manga_most_clicked,
        'updated_manga': manga_updated,
        'new_manga': manga_new,
        'alerts': alert.objects.all().order_by('-id'),
        'random': mangax,

               }


    return render(request,template,context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def manga_info(request,m_slug):
    manga.objects.filter(manga_slug=m_slug).update(manga_views=F('manga_views')+1)
    all_genres = genre.objects
    manga_object = get_object_or_404(manga,manga_slug=m_slug)
    chapters = chapter.objects.filter(chapter_manga=manga_object).order_by('-chapter_added').exclude(Q(chapter_number__icontains="-eng-li")).exclude(Q(chapter_number__icontains="-fr-li")).exclude(Q(chapter_number__icontains="ar-li"))
    template = 'manga/manga.html'
    top_ = manga.objects.all().order_by('-manga_views')[0:12]

    try:

        if "," in manga_object.manga_genres:
            manga_tag_ = manga_object.manga_genres.split(",")
            manga_tag = list(filter(None, manga_tag_))
        else:
            manga_tag = []
            manga_tag.append(manga_object.manga_genres)
            manga_tag = list(filter(None, manga_tag))
    except:
        pass

    try:
        if ',' in manga_object.manga_authors:
            manga_authors_ = manga_object.manga_authors.split(',')
            manga_authors = list(filter(None, manga_authors_))
        else:
            manga_authors = []
            manga_authors.append(manga_object.manga_authors)
            manga_authors = list(filter(None, manga_authors))

    except:
        pass

    try:
        if ',' in manga_object.manga_other_names:
            manga_other_names_ = manga_object.manga_other_names.split(',')
            manga_other_names = list(filter(None, manga_other_names_))
        else:
            manga_other_names = []
            manga_other_names.append(manga_object.manga_other_names)
            manga_other_names = list(filter(None, manga_other_names))

    except:
        pass


    top = manga.objects.all().order_by('-manga_views')[0:10]


    ip_current_user = get_client_ip(request)
    students = manga.objects.all()
    for i in range(500):
        mangax = random.choice(students)

    if ip_rate.objects.filter(connection__rate_manga__manga_slug=m_slug,ip_of_rater=ip_current_user).exists():
        User_Post_Ip = None
    else:
        User_Post_Ip = ip_current_user
    try:
        hearts = ip_rate.objects.filter(connection__rate_manga__manga_slug=m_slug).count()
    except:
        hearts = None

    eng = chapter.objects.filter(chapter_manga=manga_object,chapter_number__icontains='-eng-li')
    fr = chapter.objects.filter(chapter_manga=manga_object,chapter_number__icontains='-fr-li')
    ar = chapter.objects.filter(chapter_manga=manga_object,chapter_number__icontains='ar')

    connection.close()

    context = {'recomend':top_,'manga': manga_object, 'genres':all_genres, 'tags': manga_tag, 'chapters': chapters,
               'author': manga_authors, 'top': top,'other': manga_other_names,'random': mangax, 'ip': User_Post_Ip, 'heart': hearts,
               'chapters_eng': eng, 'chapters_fr': fr, 'chapters_ar': ar}

    return render(request, template, context)





def get_prev_next(obj, qset):
    assert obj in qset
    qset = list(qset)
    obj_index = qset.index(obj)
    try:
        previous = qset[obj_index-1]
    except IndexError:
        previous = None
    try:
        next = qset[obj_index+1]
    except IndexError:
        next = None
    return previous,next

def chapter_read(request,c_slug):
    template = 'chapter/chapter.html'

    chapter_object = get_object_or_404(chapter,chapter_slug=c_slug)

    manga_object = manga.objects.get(manga_slug=chapter_object.chapter_manga.manga_slug)

    chapter_objects_all = chapter.objects.filter(chapter_manga__manga_slug=manga_object.manga_slug).order_by('-id')

    try:
        old_index = list(chapter.objects.filter(chapter_manga__manga_slug=manga_object.manga_slug).order_by('-id')).index(chapter_object) + 1
        old = chapter_objects_all[old_index]
    except:
        old = ''

    try:
        new_index = list(chapter.objects.filter(chapter_manga__manga_slug=manga_object.manga_slug).order_by('-id')).index(chapter_object) - 1
        next = chapter_objects_all[new_index]
    except:
        next = ''




    r = requests.head("https://frtoon08.com", allow_redirects=True)
    url = r.url.replace("https://", '').replace(".com/", "")






    img = chapter_object.chapter_links.split("|")
    item = manga.objects.all().order_by('-manga_views')[0:10]
    index = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
    index.reverse()
    top = list(zip(item,index))

    chapter_images = []
    for links in img:
        if 'frtoon' in links:
            index = links.split('.com')[0].split('https://')[-1].split('.')[-1]
            chapter_images.append(links.replace(index, url))
        else:
            chapter_images = img



    images_num = []
    for i in range(len(chapter_images)):
        images_num.append(i)

    chapter_images = zip(chapter_images,images_num)

    chapter_cant = chapter.objects.filter(chapter_manga__manga_slug=manga_object.manga_slug)


    context = {
                'images': chapter_images,
                'manga': manga_object,
                'chapter_list': chapter_cant,
                'chapter': chapter_object,
                'old': old,
                'next': next,
                'top': top,
                'list': chapter_objects_all,
                'fruri': url,
               }
    connection.close()

    return render(request, template, context)




def search(request):
    students = manga.objects.all()
    for i in range(500):
        mangax = random.choice(students)
    if request.GET.get('search', None):
        template = 'browse/browse_search.html'
        mangas = manga.objects.filter(manga_name__icontains=request.GET['search'])
        connection.close()
        context = {'manga':mangas,'search': request.GET['search'],'random':mangax,'genres': genre.objects.all()}
        return render(request,template,context)
    else:
        template = 'result/search.html'
        return render(request, template, {'random': mangax})


def not_found_error(request, exception):
    template = '404.html'
    return render(request,template)

def browse(request):
    students = manga.objects.all()
    for i in range(500):
        mangax = random.choice(students)
    if request.GET.get('author', None):
        template = 'browse/browse_author.html'
        author = request.GET['author']
        manga_objects = manga.objects.filter(manga_authors__icontains=author)
        connection.close()

        context = {'author': author,
                   'manga': manga_objects,
                   'genres': genre.objects.all,
                   'current_genre': '',
                   'random': mangax
                   }
        return render(request, template, context)



    else:
        template = 'browse/browse.html'
        try:
            data = request.GET['genre']
        except:
            data = 'All'

        if data == 'All':
            manga_objects = manga.objects.all()
        else:
            manga_objects = manga.objects.filter(manga_genres__icontains=data)
        connection.close()

        print(manga_objects)

        ammount = Paginator(manga_objects, 26)

        try:
            page_num = request.GET.get('results', '1')
        except Exception:
            page_num = 1
        try:
            manga_results = ammount.page(page_num)
        except:
            manga_results = ammount.page(ammount.num_pages)



        context = {
            'manga': manga_results,
            'genres': genre.objects.all,
            'current_genre': data,
            'random': mangax
        }

        return render(request, template, context)

def shine(request, slug):
    students = manga.objects.all()
    for i in range(500):
        mangax = random.choice(students)
    item = get_object_or_404(alert,alert_slug=slug)
    template = 'result/alert.html'
    alert.objects.filter(alert_slug=item.alert_slug).update(alert_clicks=F('alert_clicks') + 1)
    return render(request,template,{'alert': item, 'random': mangax})
