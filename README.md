# Updated for Python v3.10
## Overview

This is a project to maintain a record for changes from Google's Knowledge Panel by parsing keywords using `xpath`, 
`BeautifulSoup`, and `lxml`. Moreover, there will be explanation here for those functions to update, view, or parse 
queries.  

### Usage

**_Note:_** We now use a local object to store data for all business name. Therefore, there will be a file named 
`output.json` which contains the local dataset for all business name that are visited. 

There are two python files - `main.py` and `gmbLocation.py`.  All major functions are in `main.py` with the GmbLocation 
class for parsing and saving data from/to local dataset in `gmbLocation.py`


## Working With "Locations"
Locations are defined by a 'query' that will populate a Knowledge Graph of a busines/location.  Examples of these are 
usually branded like `ACME Industries LLC Oakland CA` or `ACME Ind Oakland`. Situations can arise where a *location* not 
popping a KG is the symptom of a GMB/GBP listing issue.

#### ! Adding Locations !

#### Update Function
We first need to initiate the GmbLocation class in order to read the local dataset and pass it to the `updateLocalObject` 
function.

```sh
import gmbLocation as gmbL
from main import updateLocalObject

g = gmbL.GmbLocation()
local_obj = g.readFile() 
updateLocalObject('BMW of Las Vegas', local_obj[0])
```

#### Parse Function

```sh
parse('2023-01-29', 'BMW of Las Vegas') 
```

The parse function will return an obj that contains google_serp_url,time, image, business_name, address, category_snippet, website,phone_number, and departments. For example, 

```sh

{'address': '6900 W Sahara Ave, Las Vegas, NV 89117',
 'business_name': 'BMW of Las Vegas',
 'category_snippet': 'BMW dealer in Las Vegas, Nevada',
 'departments': 'BMW of Las Vegas Parts Center\xa0·\xa0BMW of Las Vegas '
                'Service Center',
 'google_serp_url': 'https://google.com/search?q=BMW of Las Vegas',
 'image': ['/logos/doodles/2023/celebrating-bubble-tea-6753651837109839.4-sh.png',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
           'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='],
 'phone_number': '(702) 570-0279',
 'time': '2023-01-29',
 'website': 'https://www.bmwvegas.com/?utm_source=local&utm_medium=organic&utm_campaign=*000012247*GMB'}
```

#### View Function 

```sh
findLast30Days(local_obj, 'BMW of Las Vegas', 30)
```

This function can look up information of the business name for the last 30 days. In addition, it can be any number. For 
example, it can be pulled out information for the last 2000 days of the business name. 

!TODO: touch on testing the BS4 setup, to make sure they can get a page
!TODO: Adding a business/location to be checked
!TODO: How the regular checking works (shell script/ec2/etc, doesn't need to be detailed)
!TODO: Summary feature, we need something that will summarize changes over time by a location/business, eg: BMW of Las Vegas had 6 image changes in the last 30 days, BMW of Austin had 1 image change and a category change

