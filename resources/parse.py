# currently only supports processing KP results from Google.

class ScrapeParser(html_text_content=None, parse_type=None):
    parse_types = ['local_google_kp']

    def __init__(self):
        import lxml

        self.job_settings = {
            'parse_type': parse_type,
            'content': html_text_content
        }
        return

    def parse(self, parse_type='local_google_kp'):

        self.job_settings['parse_type'] = parse_type  # <--- temp until other parsers are implemented

        if self.job_settings['parse_type'] == 'local_google_kp':

            ### XPATHs for Desktop Local Business KP
            element_xpaths = {
                'image_url': '//g-img[@class="ZGomKf"]/img/@src',
                'business_name': '//div[@class="fYOrjf kp-hc"]//h2/span/text()',
                'address': '//div[@class="UDZeY OTFaAf"]//div[@class="QsDR1c"]//span[@class="LrzXr"]',
                'category_snippet': '//span[@class="YhemCb"]',
                'website': '//a[@class="ab_button"]/@href',
                'phone_number': '//div[@class="UDZeY OTFaAf"]//div[@class="QsDR1c"]//a[@data-dtype]',
                'departments': '//div[@data-hveid="CNkBEAA"]/div/span[2]'
             }

        # process the tree content
        tree = ScrapeParser.create_html_tree(self.job_settings['content'])
        extract_output = {}

        for k, v in element_xpaths:
            extract_output[k] = get_xpath_item_from_tree(tree, v)

        return extract_output

    @staticmethod
    def create_html_tree(html_text_content):
        # simply takes text and turns it into an HTML tree we can xpath against
        from lxml import etree
        return etree.parse(html_text_content)

    @staticmethod
    def get_xpath_item_from_tree(html_tree, xpath):
        # takes soup and xpath and returns the value(s)
        return html_tree.xpath(xpath)
