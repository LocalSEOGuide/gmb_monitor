import json
import os.path

# Setup Gdrive Files
## create reporting setup (user input)


# Job handling logic
## continuing existing job
## setting up new job
## saving job info for on-going

# Reporting
## notifying users of imports changes


# check listings


class GmbMonitor(sheet_id=None):
    """
    Object used to create the data used for reporting; this object pulls several parts of the tool together and
    grabs the SERP data from the selected scraper and dumps the data locally (or in gsheets).
    """
    import datetime as dt

    def __init__(self):
        self.input_data = None
        self.scraper = None
        self.params = {
            "report": None,
            "needs_setup": None,
            "timestamp": dt.datetime.today().strftime("%m-%d-%Y")
        }

        if sheet_id:
            # load existing monitoring job
            print("Loading monitoring project: {}".format(sheet_id))

        return

    def init_scraper(self):
        import resource.scrape_integration as si

        self.scraper = si.SerpScraper('scrapyAPI')  # update to different scraper methods as needed

    def get_gmb_data(self):
        return


class MonReport:
    # handle all reporting/comparison from monitor scraping
    def __init__(self):
        return

    def init_reporting(self):
        return

    def create_reporting(self):
        return

    def continue_reporting(self):
        return

    def run_reporting(self):
        return

    def output_reporting_record(self):
        return








































