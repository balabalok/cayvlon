import requests
from bs4 import BeautifulSoup
from manga.models import chapter,manga
class manga_chapter_madara(object):
    def __init__(self, url):
        self.url = url
        self.url_list = []

    def manga_add(self,image,name,alt,aut,sta,tag,desc,slg):
        if manga.objects.filter(manga_name=name).exists():
            print(f"Manga {name} Already Exists Checking For Chapters.")
            return manga.objects.get(manga_name=name)
        else:
            new_manga = manga()
            new_manga.manga_cover_url = image
            new_manga.manga_name = name
            new_manga.manga_authors = aut
            new_manga.manga_other_names = alt
            new_manga.manga_status = sta
            new_manga.manga_genres = tag
            new_manga.manga_descrition = desc
            new_manga.manga_slug = slg
            new_manga.save()

            print(f"Manga {name} Added.")
            return manga.objects.get(manga_name=name)

    def manga_image(self, source):
        code = requests.get(self.url).text
        soup = BeautifulSoup(code, 'lxml')
        find = soup.find("div", {'class': 'summary_image'})
        print(find.img.get('data-src'))
        return find.img.get('data-src')

    def manga_name(self, source):
        code = requests.get(self.url).text
        soup = BeautifulSoup(code, 'lxml')
        find = soup.find("div", {'class': 'post-title'})
        return find.h1.text.strip()

    def manga_alt(self, source):
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find_all("div", {'class': 'summary-content'})
        return find[2].text.strip()

    def manga_authors(self, source):
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find("div", {'class': 'author-content'})
        list_ = []
        for urls in find.find_all('a'):
            list_.append(urls.text)
        return ','.join(list_)

    def manga_status(self, source):
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find_all("div", {'class': 'summary-content'})
        return find[-1].text.strip()

    def manga_tags(self, source):
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find("div", {'class': 'genres-content'})
        list_ = []
        for urls in find.find_all('a'):
            list_.append(urls.text)
        return ','.join(list_)

    def description(self, source):
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find("div", {'class': 'summary__content'})
        return find.text

    def chapter_slug_checker(self):
        count_of_chapters_in_the_manga = chapter.objects.filter(chapter_manga__manga_slug=self.manga.manga_slug).count()
        id_accession = count_of_chapters_in_the_manga+1
        return self.manga.manga_name + '-Chapter-' + str(id_accession)

    def manga_slug(self,name):
        if ' ' in name:
            new_name = name.replace(' ', '-')
        else:
            new_name = name
        count = str(manga.objects.count())
        slug = new_name +'-'+count
        return slug


    def chapter_add(self, chapter_n,chapter_s):

        if chapter.objects.filter(chapter_manga=self.manga,chapter_number=chapter_n).exists():
            print(f"Manga {self.manga.manga_name} Chapter: {chapter_n} Exists Skipping.")
        else:

            new_chapter = chapter()

            new_chapter.chapter_number = chapter_n
            new_chapter.chapter_links = chapter_s
            new_chapter.chapter_manga = self.manga
            slug_returned = self.chapter_slug_checker()
            new_chapter.chapter_slug = slug_returned

            new_chapter.save()

            print(f"Manga {self.manga.manga_name} Chapter - {chapter_n} [ADDED]")



    def chapter_scrapper(self):
        source = requests.get(self.url).text

        soup = BeautifulSoup(source, 'lxml')
        data = soup.find('ul', {'class': 'main version-chap'})
        list_links = []
        for items in data.find_all('a'):
            self.url_list.append(items.get('href'))

        self.url_list.reverse()
        return self.url_list

    def scraper_chapter_images(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        find = soup.find_all('img', {'class': 'wp-manga-chapter-img img-responsive lazyload effect-fade'})
        list_ = []
        for items in find:
            list_.append(items.get('data-src'))

        fresh = [items.strip() for items in list_]
        return '|'.join(fresh)

    def scrape_chapter_number(self,url):
        link_splitted = url.split("chapter-")
        last_catch = link_splitted[-1]
        if "/" in last_catch:
            final_var = last_catch.replace('/', '')
        else:
            final_var = last_catch

        return final_var

    def dataCollector(self,url):

        image_string = self.scraper_chapter_images(url)
        c_number = self.scrape_chapter_number(url)

        self.chapter_add(c_number,image_string)

    def dataCollector_manga(self):

        data_source = requests.get(self.url).content

        manga_img = self.manga_image(data_source)
        manga_nm = self.manga_name(data_source)
        manga_alt = self.manga_alt(data_source)
        manga_aut = self.manga_authors(data_source)
        manga_st = self.manga_status(data_source)
        manga_tg = self.manga_tags(data_source)
        manga_des = self.description(data_source)
        manga_slg = self.manga_slug(manga_nm)

        self.manga_add(manga_img,manga_nm,manga_alt,manga_aut,manga_st,manga_tg,manga_des,manga_slg)

    def name(self):
        data_source = requests.get(self.url)
        manga_nm = self.manga_name(data_source)

        object_ = manga.objects.get(manga_name=manga_nm)
        return object_

    def name_send(self):
        data_source = requests.get(self.url)
        manga_nm = self.manga_name(data_source)
        return manga_nm


    def chapter_sender(self):

        self.dataCollector_manga()
        self.manga = self.name()

        self.chapter_scrapper()

        for items in self.url_list:
            self.dataCollector(items)

