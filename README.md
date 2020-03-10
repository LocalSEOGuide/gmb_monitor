# Overview
Monitors Knowledge Graphs by taking a list of brand searches, queries Google, checks for the Knowledge Graph (KG) and records the image.  It then takes the previous day's results and compares the images; results that have changed are flagged with a `'1'` in the `'data'` tab and the records are placed in a sheet called `'image_change_tracking'`.

The script is intended to be ran everyday.  This can be accomplished by running it local manually (*Ewww*), [setting up a batch file (windows) + task schedule](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279) to run automagically, or [adding proxies](https://wonderproxy.com/blog/a-step-by-step-guide-to-setting-up-a-proxy-in-selenium/) to the `get_serp(url)` function's use of Selenium and throwing it on an EC2 instance + cronjob. 

## Setup
Create your virtual using the environment.yml file associated with the repo.  It makes use of Gsheets API via the `gspread` library as well as `Selenium` + `BeautifulSoup` to get the Google SERP and `pandas` to handle/compare data.  After your enivonrment is setup, you'll need to get [serviceaccount credentials](https://gspread.readthedocs.io/en/latest/oauth2.html) through the [Google's Developer Console](https://console.developers.google.com/) saving the credentials as `client_secret.json` in the script's directory. You'll also need `chromedriver.exe` in the scripts path, which you can get from [here](https://chromedriver.chromium.org/downloads) 

Once you've setup the script to work, create a new gsheet ([example](https://docs.google.com/spreadsheets/d/19aUd0J6Kb5_Gyp0kIl8zqy8FpjeKE-2FV5HZ4tpHI_U/edit#gid=1292770253)) with the following tabs: 
* data (stores all historical data)
   * 1 row + 5 columns, With these headers: `Business Name`, `google_query`, `kg_image_url`, `timestamp`, `change_detected`
* image_change_tracking (store only records where images changed)
    * 1 row + 5 columns, with these headers: `Business Name`, `date_discovered`, `google_query`, `new_kg_image_url`, `old_kg_image_url`
* brands_to_query (the brands to query)
    * 1 column with this header: `Business Name`
    
...update the `gsheet_workbook_name` variable to your sheet's name and invite your `serviceaccount` with edit privileges (*its address will be something like: the-name-you-gave-it@gsheets-205000.iam.gserviceaccount.com*). 

## Note From Heckler
This thing was written originally 2 years ago, it was an adventure figuring out what everything did a couple years removed (*thank god for comments*) and there's some cringe worthy code here; I'll improve it overtime (*like removing terrible itterators eg- `range(len(df))`*).  If you have problems just hit me up on [Twitter](https://twitter.com/hecklerponics) and/or fork it. 
