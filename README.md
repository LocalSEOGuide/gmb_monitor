# Updated for Python v3.10
## Overview

This is a project to maintaint a record for changes from knowledge panel on google search result by parsing keywords using xpath, BeautifulSoup, and lxml. Moreover, there will be explaination here for those functions to update, view, or parse queries.  

### Usage

#### Note

Now we use a local object to store data for all business name. Therefore, there will be a file named output.json which contains the local dataset for all business name that are visited. 

#### Update Function 

We first need to initiate the GmbLocation class in order to read the local dataset and pass it to the updateLocalObject function.

```sh
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

This function can look up information of the business name for the last 30 days. In addition, it can be any number. For example, it can be pulled out information for the last 2000 days of the business name. 



