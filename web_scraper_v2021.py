import requests


class Scraper:
    def __init__(self, header, error):
        self.url = None
        self.header = header
        self.error = error

    def get_input(self):
        self.url = input()

    def get_response(self):
        r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if r.status_code == 200:
            return r
        print(self.error)
        exit()

    def get_quote(self):
        r_json = self.get_response().json()
        return r_json.get(self.header, self.error)

    def main(self):
        self.get_input()
        quote_or_error = self.get_quote()
        print(quote_or_error)


search = 'content'
fail = 'Invalid quote resource!'

my_scraper = Scraper(search, fail)
my_scraper.main()
