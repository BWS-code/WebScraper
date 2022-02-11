import requests


class Scraper:
    def __init__(self, filename):
        self.url = None
        self.filename = filename


    def get_input(self):
        self.url = 'https://www.imdb.com/title/tt0080684/'

    def get_content(self):
        r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if r.status_code == 200:
            return r.content
        print(f'The URL returned {r.status_code}')
        return None


    def save_to_file(self, name, what):
        with open(name, 'wb') as f:
            f.write(what)
        print('Content saved.')

    def main(self):
        self.get_input()
        content = self.get_content()
        if content:
            self.save_to_file(self.filename, content)


file = 'source.html'

my_scraper = Scraper(file)
my_scraper.main()
