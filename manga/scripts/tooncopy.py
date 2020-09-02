import requests
from bs4 import BeautifulSoup
from manga.models import manga,chapter
from slugify import slugify

class copytoon(object):
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
        src = requests.get(f"{link}")
        soup = BeautifulSoup(src.content, 'lxml')
        find_data = soup.find('div', id='bo_v_con')
        img_lis = []
        for urls in find_data.find_all('img'):
            img_lis.append(urls.get('src'))
        data_fix = '|'.join(img_lis)
        return data_fix

    def chapter_number(self, link):
        if '화' in requests.get(link).text:
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            data = soup.title.text.split("화")
            return data[0]
        else:
            chapter_filter = chapter.objects.filter(chapter_manga__manga_slug=self.slug).count()
            num = int(chapter_filter) + 1
            return str(num)

    def manga_chapters(self):
        src = requests.get(self.m_link)
        soup = BeautifulSoup(src.content, 'lxml')
        find_data = soup.find('div', {'role': 'tabpanel'})
        for chapters in find_data.find_all('a'):
            self.chapters_list.append(chapters.get('href'))

    def chapter_slug(self, num):
        sl = slugify(self.manga_object.manga_name + '-chapter-' + num)
        return sl


    def worker(self, link):
        chapter_number = self.chapter_number(link)
        chapter_images = self.chapter_scrapper(link)
        chapter_slug = self.chapter_slug(chapter_number)

        self.chapter_adder(chapter_number, chapter_slug, chapter_images)

    def start(self):
        print("Started")
        self.manga_chapters()
        self.chapters_list.pop(0)
        self.chapters_list.reverse()
        for chapters in self.chapters_list:
            self.worker(chapters)


