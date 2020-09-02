import requests
from bs4 import BeautifulSoup
from manga.models import manga,chapter
from slugify import slugify

class mh123(object):
    def __init__(self, manga_link, slug):
        self.m_link = manga_link
        self.chapters_list = []
        self.slug = slug
        self.manga_object = manga.objects.get(manga_slug=self.slug)

    def chapter_adder(self,number,slug,image):
        if chapter.objects.filter(chapter_manga__manga_slug=self.slug,chapter_number=number).exists():
            print(f"Chapter {number} Skipped.")
        else:
            new_chapter = chapter()
            new_chapter.chapter_manga = self.manga_object
            new_chapter.chapter_number = number
            new_chapter.chapter_slug = slug
            new_chapter.chapter_links = image
            new_chapter.save()

            print(f"Chapter {number} Added.")

    def chapter_scrapper(self, link):
        source = requests.get(f"{link}")
        soup = BeautifulSoup(source.text, 'lxml')
        data = soup.find_all('script')
        path = data[2].text.split(';var chapterPath = "')[1].split('";var pageTitle')[0]

        split = data[2].text.split('chapterImages = ')
        image_list = split[-1].split(';')[0].replace('[', '').replace(']', '').split(',')
        fixed_image_list = []
        for items in image_list:
            fixed_image_list.append(f"https://img.wszwhg.net/{path}" + items.replace('"', ''))

        return '|'.join(fixed_image_list)

    def chapter_number(self, link):
        source = requests.get(f"{link}")
        soup = BeautifulSoup(source.text, 'lxml')
        return '['+soup.h1.text+']'+f'-{str(chapter.objects.filter(chapter_manga__manga_name=self.manga_object.manga_name).count() + 1)}'

    def manga_chapters(self):
        source = requests.get(self.m_link)
        soup = BeautifulSoup(source.text, 'lxml')
        find = soup.find('ul', id="chapter-list-1")
        for links in find.find_all('a'):
            self.chapters_list.append("https://www.mh1234.com" + links.get('href'))

    def chapter_slug(self, num):
        return slugify(self.manga_object.manga_slug + '-chapter-' + num)


    def worker(self, link):
        chapter_number = self.chapter_number(link)
        chapter_images = self.chapter_scrapper(link)
        chapter_slug = self.chapter_slug(chapter_number)

        self.chapter_adder(chapter_number, chapter_slug, chapter_images)

    def start(self):
        self.manga_chapters()
        for chapters in self.chapters_list:
            self.worker(chapters)

