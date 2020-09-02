import requests
from bs4 import BeautifulSoup
from manga.models import chapter,manga


class manga_and_chapter_mangakaka(object):
    def __init__(self, url, slug):
        self.url = url
        self.chapter_list = []
        self.manga_object = manga.objects.get(manga_slug=slug)



    def chapter_add(self, chapter_n,chapter_s):

        if chapter.objects.filter(chapter_manga=self.manga_object,chapter_number=chapter_n).exists():
            print(f"Manga {self.manga.manga_name} Chapter: {chapter_n} Exists Skipping.")
        else:

            new_chapter = chapter()

            new_chapter.chapter_number = chapter_n
            new_chapter.chapter_links = chapter_s
            new_chapter.chapter_manga = self.manga_object

            new_chapter.save()

            print(f"Manga {self.manga_object.manga_name} Chapter - {chapter_n} [ADDED]")



    def chapter_scrapper(self):

        source = requests.get(self.url).text
        soup = BeautifulSoup(source, 'lxml')
        soup_chapter_div = soup.find('div', {'class': 'chapter-list'})
        row = soup_chapter_div.find_all('a')
        row.reverse()

        for items in row:
            self.chapter_list.append(items.get('href'))

    def scraper_chapter_images(self, url):
        list_links = []

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')


        soup_div = soup.find('div', {'class': 'vung-doc'})
        soup_image_list = soup_div.find_all('img')
        for links in soup_image_list:
            list_links.append(str(links.get('src')))

        string_image = '|'.join(list_links)
        return string_image

    def scrape_chapter_number(self,url):
        chapter_num = url.split("chapter_")[-1]
        return chapter_num + '-eng-li'

    def dataCollector(self,url):

        image_string = self.scraper_chapter_images(url)
        c_number = self.scrape_chapter_number(url)

        self.chapter_add(c_number,image_string)


    def chapter_sender(self):


        self.chapter_scrapper()

        for items in self.chapter_list:
            self.dataCollector(items)
