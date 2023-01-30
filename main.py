# currently only supports processing KP results from Google.
from datetime import date , timedelta
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import pprint as pp
import gmbLocation as gmbL
import os
import pandas as pd

# function to search for history 
# toDO: fix name of num
def findLast30Days(local_obj,name, numOfDay): 
    # inner function
    def setDict(url='', address='', business_name='', category_snippet='', departments='', image='', phone_number='', current_visit_time='', website='', changes='', lastVisited=''):
        out_dict = {
            'URL': url,
            'address': address,
            'business_name': business_name,
            'category_snippet': category_snippet,
            'departments': departments, 
            'image': image,
            'phone_number': phone_number,
            'current_visit_time': current_visit_time,
            'website': website,
            'changes': changes,
            'lastVisited': lastVisited,
        }
        return out_dict

    flag, alist = False, []

    targetTime = None
    while num > 0:
        targetTime = (date.today()-timedelta(num)).isoformat()
        if targetTime in local_obj['business_name'][name]['content']:
            break
        num -= 1 

    if targetTime == None:
        return [] 

    for key in local_obj['business_name'][name]['content']: 
        if key == targetTime: 
            flag = True 
        if flag:
            c = local_obj['business_name'][name]['content'][key]

            total_changes = 0
            for change in local_obj['business_name'][name]['changeSinceLastVisited'][key]: 
                if change != 'google_serp_url' and change != 'lastVisitedDate':

                    total_changes += local_obj['business_name'][name]['changeSinceLastVisited'][key][change]
            last_visited = local_obj['business_name'][name]['changeSinceLastVisited'][key]['lastVisitedDate']

            alist.append(setDict(
                                    url=c['google_serp_url'],
                                    address=c['address'],
                                    business_name=c['business_name'],
                                    category_snippet=c['category_snippet'],
                                    departments=c['departments'],
                                    image=c['image'],
                                    phone_number=c['phone_number'],
                                    current_visit_time=c['time'],
                                    website=c['website'],
                                    changes=total_changes,
                                    lastVisited=last_visited,
                                )
                        )

    df = pd.DataFrame(alist)
    df.to_csv(name + '_history.csv')



# function to update local dataset and return changes 
def updateLocalObject(name, local_obj):

    # using a inner function to generate attributes for changes
    def generate_change_attribute():
        return {
                    'google_serp_url': '', 
                    'address_changes'  :  0, 
                    'business_name_changes': 0,
                    'category_snippet_changes' :0,
                    'departments_changes': 0, 
                    'image_changes': 0,
                    'phone_number_changes': 0,
                    'website_changes': 0,
                    'lastVisitedDate':'',
        }

    timeStamp = date.today().isoformat()
    # lastVisited = local_obj['business_name'][name]['timeVisited'][-1]
    res = parse(timeStamp,name)

    if not res:
        return local_obj
    
    if name not in local_obj['business_name']:
        local_obj['business_name'][name] = {} 
        local_obj['business_name'][name]['google_serp_url'] = res['google_serp_url'] 
        local_obj['business_name'][name]['timeVisited'] = set()
        local_obj['business_name'][name]['content'] = {}
        local_obj['business_name'][name]['changeSinceLastVisited'] = {}

    local_obj['business_name'][name]['timeVisited'].add(timeStamp)
    local_obj['business_name'][name]['content'][timeStamp] = res

    # if this business name was visited before, then starting to compare with the current visit one
    if len(local_obj['business_name'][name]['timeVisited']) > 0 and next(iter(local_obj['business_name'][name]['timeVisited'])) != timeStamp:

        # find content from last visited 
        lastVisited = next(iter(local_obj['business_name'][name]['timeVisited']))
        content_from_lastVisited = local_obj['business_name'][name]['content'][lastVisited] 
        local_obj['business_name'][name]['changeSinceLastVisited'][timeStamp] = generate_change_attribute() 
        local_obj['business_name'][name]['changeSinceLastVisited'][timeStamp]['google_serp_url'] = res['google_serp_url']
        changes = local_obj['business_name'][name]['changeSinceLastVisited'][timeStamp]

        # start comparing current content and last visited content 
        for element in res: 
            if res[element] != content_from_lastVisited[element] and element != 'time':
                ele = element + '_changes'
                changes[ele] += 1 

        # Update last visited date to today
        local_obj['business_name'][name]['timeVisited'][0] = timeStamp
        changes['lastVisitedDate'] = lastVisited
        local_obj['business_name'][name]['changeSinceLastVisited'][timeStamp] = changes

    return local_obj

# parse key components from google search result and return a dictionary 
def parse(timeStamp,business_name):


    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }

    page = requests.get(
        'https://google.com/search?q=' + business_name,
        headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    time.sleep(7)
    dom = etree.HTML(str(soup))
    res = {} 

    # Google:
    res['google_serp_url'] = 'https://google.com/search?q=' + business_name
    # Time: 
    res['time'] = timeStamp

    # image:
    res['image'] = dom.xpath('//g-img[@class="ZGomKf"]/img/@src')
    # business_name
    res['business_name'] = dom.xpath('//div[@class="fYOrjf kp-hc"]//h2/span/text()')[0]
    # address
    res['address'] = dom.xpath('//div[@class="UDZeY OTFaAf"]//div[@class="QsDR1c"]//span[@class="LrzXr"]')[0].text
    # category_snippet
    res['category_snippet'] = dom.xpath('//span[@class="YhemCb"]')[0].text
    # website
    res['website'] = dom.xpath('//a[@class="ab_button"]/@href')[0]
    # phone_number
    res['phone_number'] = soup.find( "span" , class_='LrzXr zdqRlf kno-fv').text 
    # departments
    res['departments'] = soup.find( "span" , class_='ZcbhQc').text

    return res





