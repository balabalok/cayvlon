import requests
from bs4 import BeautifulSoup
from manga.models import manga,chapter
from slugify import slugify

class madara(object):
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
        src = requests.get(link)
        soup = BeautifulSoup(src.text, 'lxml')
        find = soup.find('div', {'class': 'reading-content'})
        link = []
        for links in find.find_all('img'):
            link.append(links.get('data-src'))

        str = '|'.join(link).replace(' ', '')
        return str.strip().rstrip()

    def chapter_number(self, link):
        if '-' in link:
            strip = link.split('chapter-')
            if '/' in strip[-1]:
                return strip[-1].replace('/', '')
            else:
                return strip[-1]
        else:
            chapter_filter = chapter.objects.filter(chapter_manga__manga_slug=self.slug).count()
            num = int(chapter_filter) + 1
            return str(num)

    def manga_chapters(self):
        src = requests.get(self.m_link)
        soup = BeautifulSoup(src.text, 'lxml')
        soup_li = soup.find('ul', {'class': 'main version-chap'})
        for links in soup_li.find_all('a'):
            self.chapters_list.append(links.get('href'))

    def chapter_slug(self, num):
        return slugify(self.manga_object.manga_name + '-chapter-' + num)


    def worker(self, link):
        chapter_number = self.chapter_number(link)
        chapter_images = self.chapter_scrapper(link)
        chapter_slug = self.chapter_slug(chapter_number)

        self.chapter_adder(chapter_number, chapter_slug, chapter_images)

    def start(self):
        self.manga_chapters()
        self.chapters_list.reverse()
        for chapters in self.chapters_list:
            self.worker(chapters)

