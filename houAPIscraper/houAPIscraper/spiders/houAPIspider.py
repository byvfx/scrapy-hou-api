import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    # custom_settings = {'CLOSESPIDER_TIMEOUT': 60}
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/index.html",
                  "https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html"]

    # rules = (
    #     Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_start_url',follow=True),
    #     Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/BaseKeyframe.html')), callback='parse_item'),
    #     )

    def parse_start_url(self, response):
        return self.parse_item(response)
    
    def parse_item(self, response):
        print(f"Processing URL: {response.url}")
        data = {
            'title': 'hou package',
            'categories': []
        }

        categories = response.xpath('//section[contains(@class, "heading pull left")]')
        for category in categories:
            category_name = category.xpath('./h2[@class="label heading pull left"]/@data-title').get()
            print(f"Category Name: {category_name}")
            category_data = {
                'name': category_name,
                'items': []
            }

            items = category.xpath('.//li[contains(@class, "subtopics_item")]')
            for item in items:
                item_title = item.xpath('./p[@class="label"]/a/text()').get()
                item_summary = item.xpath('./p[@class="summary"]/text()').get()

                item_data = {
                    'title': item_title,
                    'summary': item_summary,
                    'functions': []
                }

                # Extract the methods within this category item
                function_selectors = item.xpath('.//div[contains(@class, "collapsible method item collapsed")]')
                for function_selector in function_selectors:
                    function_name = function_selector.xpath('./@data-title').get()
                    function_description_parts = function_selector.xpath('./following-sibling::div[contains(@class, "content")]/p//text()').getall()
                    function_description = ' '.join([desc.strip() for desc in function_description_parts]).replace('\n', ' ')
                    function_description = re.sub(' +', ' ', function_description)

                    # Extract code examples if any
                    code_parts = function_selector.xpath('./following-sibling::div[contains(@class, "code-container")]//span/text()').getall()
                    code_text = ''.join(code_parts).replace('\n', ' ')
                    code_text = re.sub(' +', ' ', code_text)

                    function_data = {
                        'function_name': function_name,
                        'function_description': function_description,
                        'code_example': code_text,
                    }
                    item_data['functions'].append(function_data)

                category_data['items'].append(item_data)

            data['categories'].append(category_data)

        yield data