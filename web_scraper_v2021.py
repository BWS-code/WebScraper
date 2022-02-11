import requests
from bs4 import BeautifulSoup
import string
import re


class Scraper:
    def __init__(self, url, meta, category='News', readable=100):
        self.url = url
        self.cat = category
        self.pick_cls = meta['article_pick_class']
        self.body_cls = meta['article_body_class_regex']
        self.head_prop = meta['article_head_property']
        self.body_tags = meta['article_body_tags']
        self.body = None
        self.cat = category
        self.user_set_width = readable
        self.saved_list = []

    # common
    def get_soup(self):
        r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        return BeautifulSoup(r.content, 'html.parser')

    # article scope
    def get_body(self):
        def get_readable(text, width, prev_i=0):
            def get_index(t, i):
                nonlocal prev_i
                if i - prev_i > width + 1:
                    i = prev_i + width
                while not t[i] == ' ':
                    i -= 1
                prev_i = i + 1
                return i + 1
            pos_map = [0, *[get_index(text, i) for i in range(width, len(text), width)], len(text)]
            return '\n'.join(text[pos_map[i]:pos_map[i + 1]] for i in range(len(pos_map) - 1))

        self.body = ''
        article = self.get_soup().find('div', class_=re.compile(self.body_cls)).findAll(self.body_tags)
        for element in article:
            if '\n' not in element.text:
                if self.user_set_width:
                    formatted = get_readable(element.text, self.user_set_width)
                    self.body += ''.join(formatted + '\n\n')
                else:
                    non_formatted = element.text
                    self.body += ''.join(non_formatted + '\n')
        return self.body

    def get_txt_name(self):
        head = self.get_soup().find('meta', property=self.head_prop)['content'].strip()
        file_name = '_'.join(head.translate(str.maketrans('', '', string.punctuation)).split())
        return file_name

    def save_txt_file(self):
        article_name = f'{self.get_txt_name()}.txt'
        self.saved_list.append(article_name)
        with open(article_name, 'wb') as file:
            file.write(self.get_body().encode('UTF-8'))

    # on page scope
    def get_articles_links(self):
        articles_obj = self.get_soup().find_all('article')
        articles_links = [article.find('a').get('href') for article in articles_obj \
                          if article.find('span', class_=self.pick_cls).text == self.cat]
        return articles_links

    # main procedure
    def run_extractions(self):
        domain_end = [i for i, c in enumerate(self.url) if c == '/'][2]
        for article_link in self.get_articles_links():
            self.url = self.url[:domain_end] + article_link
            self.save_txt_file()
        return f'Saved articles: {self.saved_list}'


target_link = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
known_ids = {
    'article_pick_class': 'c-meta__type',
    'article_head_property': 'og:title',
    'article_body_class_regex': '.*article.*body.*',
    'article_body_tags': ('p', 'h2', 'h3')
}

my_scraper = Scraper(target_link, known_ids)
print(my_scraper.run_extractions())
