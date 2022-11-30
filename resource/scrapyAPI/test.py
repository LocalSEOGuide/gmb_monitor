class ScrapyAPI:

    def __init__(self):
        # set needed flags
        # TO DO make the path handling more robust
        import os

        self.endpoint = 'http://api.scraperapi.com'
        self.params = {
            'api_key': open(os.path.abspath('resource\\scrapyAPI\\key.txt')).read(),  # get api key
            'apiParams': {
                "autoparse": False,
                "binary_target": False,
                "country_code": "us",
                "device_type": "desktop",
                "follow_redirect": False,
                "premium": True,
                "render": False,
                "retry_404": False
            },
            'url': None
        }
        return

    def scrape_google(self, query):
        # set the object to get Google SERP results
        import urllib.parse

        self.params['url'] = "https://www.google.com/search?q="+urllib.parse.quote(query)
        return self.scrape()

    def scrape(self):
        #  fires off the scrape with whatever settings were set
        import requests as r

        if self.params['url']:
            resp = r.get(self.endpoint, params=self.params)
        else:
            print("In order to scrape a URL needs to be provided.")

        return resp.text

