# coding: utf-8
gsheet_workbook_name = "kg_img_monitor - test data"  # name of gsheet to pull, report results to
g_search = 'https://www.google.com/search?q='  # search URL for Google

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
from time import sleep
import re

todays_date = dt.datetime.today().strftime("%m-%d-%Y")

# gsheets initialization
import gspread as gs
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def get_serp(url):
    #  get the serp result to parse through
    HTMLsource = ""
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # run tool without opening a browser, comment out to troubleshoot
        chrome_options.add_argument("disable-infobars")  # disabling infobars
        chrome_options.add_argument("--disable-extensions")  # disabling extensions
        chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        HTMLsource = driver.page_source
        driver.quit()
    except Exception as e:
        print(e)
    return HTMLsource


def make_soup(serp_html):
    soup = bs(serp_html, 'lxml')
    return soup


def get_primary_kg_img(html):
    # get the URL for the primary photo
    # get the div that the KG is in
    knowledge_graph = html.find('div', class_='ifM9O')
    # grab the image URL from the KG div
    try:
        img_url = knowledge_graph.find('g-img').img['src']

    except:
        img_url = 'No Knowledge Graph Found'

    street_view_regex = re.compile(r'^\/\/(geo\d\.ggpht\.com|lh\d\.googleusercontent).*')

    if street_view_regex.match(img_url):
        img_url = "https:" + img_url

    return img_url


# authenticate with the API
def auth_with_gsheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gs.authorize(creds)
    return client


# gets the worksheet we specific and returns a dataframe
def grab_sheet_df(gsheet_workbook_name, sheet_int):
    client = auth_with_gsheets()
    sheet = client.open(gsheet_workbook_name)
    data = sheet.get_worksheet(sheet_int)
    data_sheet = get_as_dataframe(data)
    return data_sheet


def compare_prev_photo(agg_data_df):
    # see if the photo pulled from the previous run matches the latest result
    previous_day_filter = (dt.datetime.today() - timedelta(days=1)).strftime("%m-%d-%Y")
    for x in range(len(agg_data_df[agg_data_df.timestamp >= previous_day_filter])):  # ewwww bad iterator
        biz_name = agg_data_df['Business Name'][x]
        last_result = agg_data_df.loc[(agg_data_df['Business Name'] == biz_name)
                                      & (agg_data_df.timestamp == previous_day_filter)].reset_index(
            drop=True).to_dict()

        most_recent_result = agg_data_df.loc[(agg_data_df['Business Name'] == biz_name)
                                             & (agg_data_df.timestamp == todays_date)].reset_index(
            drop=True).to_dict()

        try:
            if last_result['kg_image_url'][0] == most_recent_result['kg_image_url'][0]:
                # should update where no change is present
                print('no change')
                agg_data_df['change_detected'][x] = 0
            else:
                print('change detected...')
                agg_data_df['change_detected'][x] = 1
        except:
            print("no result.")

    agg_data_df = agg_data_df.drop_duplicates().reset_index(drop=True)
    return agg_data_df


# only grabs the sheet object, does not convert to dataframe
def grab_sheet(gsheet_workbook_name, sheet_int):
    client = auth_with_gsheets()
    sheet = client.open(gsheet_workbook_name)
    data = sheet.get_worksheet(sheet_int)
    return data


def apply_gsheet_char_limit(x):  # band aid to deal with base64 encoded images and gsheet limitations
    if len(x) > 50000:
        x = x[:50000]
        return x
    else:
        return x


# get out client data to query from the gsheet.
client_list = grab_sheet_df(gsheet_workbook_name, 2)

# construct the URL for the query based on the business' name.
client_list['google_query'] = client_list['Business Name'].apply(lambda x: x.replace(" ", "+"))
client_list['google_query'] = client_list['google_query'].apply(lambda x: str(g_search + x))

# setup the column for dumping the KG URL
client_list['kg_image_url'] = ''
client_list['timestamp'] = ''

# primary loop
print("Beginning work queue...")

for name in range(len(client_list)):  # eww nasty iterator...
    result = get_serp(client_list.google_query[name])  # get the SERP to digest
    result = make_soup(result)  # make dat soup fam
    client_list['kg_image_url'][name] = get_primary_kg_img(result)  # get the KG div and then pull the img URL from it
    sleep(15)  # sleep some, google is watching.
client_list.timestamp = dt.date.today().strftime("%m-%d-%Y")

client_list.kg_image_url = client_list.kg_image_url.apply(
    lambda x: apply_gsheet_char_limit(x))  # trim strings > 50000 len

print("Work completed.")

# get the sheets we'll be pulling/adding data from/to. and get them into dataframes
output_sheet = grab_sheet_df(gsheet_workbook_name, 0).drop_duplicates().reset_index(drop=True)

# get the image change tracking sheet
reporting_sheet = grab_sheet_df(gsheet_workbook_name, 1).drop_duplicates().reset_index(drop=True)

# append our data together.
aggregate_data = pd.concat([client_list, output_sheet],
                           sort=True).drop_duplicates().reset_index(drop=True)

# get previous days results.
previous_days_result = aggregate_data[aggregate_data['timestamp'] == (dt.datetime.today() -
                                                                      timedelta(days=1)).strftime("%m-%d-%Y")]

# join today's results to yesterday's to check for changes.
img_check_df = pd.merge(client_list, previous_days_result, on='Business Name', sort=False)

# setup the reporting dataframe
reporting_df_columns = ['Business Name',
                        'google_query',
                        'new_kg_image_url',
                        'old_kg_image_url',
                        'date_discovered']

reporting_df = pd.DataFrame(columns=[reporting_df_columns])

# loop through the joined DF and call out issues when they're found to be added to the reporting DF
for index, row in img_check_df.iterrows():
    if img_check_df['kg_image_url_x'][index] == img_check_df['kg_image_url_y'][index]:
        print("all good fam.")
    else:
        #  create a record for the flagged location/brand
        print("image change detected!")

        #  build a row to add to the reporting DF while looping through all records
        change_record = pd.DataFrame([row]).rename(columns={'google_query_x': 'google_query',
                                                            'kg_image_url_x': 'new_kg_image_url',
                                                            'kg_image_url_y': 'old_kg_image_url',
                                                            'timestamp_x': 'date_discovered'})[reporting_df_columns]

        try:  # it excepts if reporting_df is blank; not pretty but it works.
            reporting_df = pd.concat([change_record, reporting_df], sort=False).reset_index(drop=True)
        except:
            print("Assigning initial values...")
            reporting_df = change_record

# loop through the joined DF and call out issues when they're found to be added to the reporting DF
for name in range(len(img_check_df)):
    #     print(img_check_df['Business Name'][name])
    if img_check_df['kg_image_url_x'][name] == img_check_df['kg_image_url_y'][name]:
        print("all good fam.")
    else:
        #  create a record for the flagged location/brand
        print("image change detected!")

        #  build a row to add to the reporting DF while looping through all records
        change_record = {'Business Name': img_check_df['Business Name'][name],
                         'google_query': img_check_df.google_query_x[name],
                         'new_kg_image_url': img_check_df.kg_image_url_x[name],
                         'old_kg_image_url': img_check_df.kg_image_url_y[name],
                         'date_discovered': todays_date}

        reporting_df = pd.concat([reporting_df, pd.DataFrame.from_dict([change_record])],  # slam it all together
                                 sort=False)

# grab the existing reporting data, take the new and append the old onto it so results appear at top.
previous_checks_data = get_as_dataframe(grab_sheet(gsheet_workbook_name, 1))

if reporting_df.empty is True:
    print("No previous data dates to check....")

else:
    reporting_df = reporting_df.append(previous_checks_data, sort=True).reset_index(drop=True)

    aggregate_data = compare_prev_photo(aggregate_data)

# >>>>>>>>>>> Push the results back up to the worksheet.

# push the results from the change records into the image_change_tracking sheet.
if reporting_df.empty is False:
    set_with_dataframe(grab_sheet(gsheet_workbook_name, 1), reporting_df.drop_duplicates().reset_index(drop=True))

else:
    print('No data to upload to change tracking...')

# make sure our columns are in order.
aggregate_data = aggregate_data[['Business Name',
                                 'google_query',
                                 'kg_image_url',
                                 'timestamp',
                                 'change_detected']].fillna('-')

# send data to the data tab spreadsheet.
set_with_dataframe(grab_sheet(gsheet_workbook_name, 0), aggregate_data.drop_duplicates().reset_index(drop=True))

print('process complete.')