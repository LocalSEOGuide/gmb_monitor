# currently only supports processing KP results from Google.

class ScrapeParser:
    parse_types = ['local_google_kp']

    def __init__(self,html_text_content=None, parse_type=None):
        import lxml

        self.job_settings = {
            'parse_type': parse_type,
            'content': html_text_content
        }
        return

    
    def parse(self, business_name, parse_type='local_google_kp'):
        self.job_settings['parse_type'] = parse_type  # <--- temp until other parsers are implemented
        if self.job_settings['parse_type'] == 'local_google_kp':

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
