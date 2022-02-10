import requests
from bs4 import BeautifulSoup
import time


class Scraper:
    def __init__(self, ids_dict, error):
        self.url = None
        self.soup = None
        self.ids_dict = ids_dict
        self.error = error

    def get_input(self, check='imdb.com/title'):
        self.url = input()
        return check in self.url

    def get_soup(self, status_code=666):
        while status_code != 200:
            r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            status_code = r.status_code
            time.sleep(0.5)
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def get_dict(self):
        my_dict = dict()
        for name, value in self.ids_dict.items():
            my_dict.setdefault(name, self.soup.find(*value).text)
        return my_dict

    def main(self):
        if self.get_input():
            self.get_soup()
            res = self.get_dict()
            print(res)
        else:
            print(self.error)


template = {
    'title': ['h1'],
    'description': ['span', {'data-testid': 'plot-xl'}]
}
fail = 'Invalid movie page!'

my_scraper = Scraper(template, fail)
my_scraper.main()
