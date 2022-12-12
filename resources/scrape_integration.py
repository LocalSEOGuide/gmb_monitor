import scrapyAPI.test as sa

class SerpScraper:
    available_scrapers = ['local', 'scrapyAPI']
    # print("Initializing Scraper")

    def __init__(self, method=None):
        print("Setting scraping method...")
        self.params = {
            'method': method
        }

        if method and (method in SerpScraper.available_scrapers):
            self.params['method'] = method
            print("Scraper method has been set to {}.".format(method))

        else:
            print("Please provide a valid method to use for the scraper.\nAvailable scrapers: \n -> {}".format(
                ", ".join(map(str, SerpScraper.available_scrapers)))
            )

            print("Otherwise the 'local' method will be used as a default.")
            self.params['method'] = SerpScraper.available_scrapers[0]

        return

    def getScrape(self, query):
        scrape = sa.scrapyAPI() 
        return scrape.scrape_google(query)



    def get_scrape(self, url=None, type='gSERP'):
        return

