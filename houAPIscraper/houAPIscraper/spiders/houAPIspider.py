import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/index.html"]

    rules = (Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_item',follow=True),)

    def parse_start_url(self, response):
        return self.parse_item(response)
    
    def parse_item(self, response):
        data = {
            'title': 'hou package', 
            'categories': []
        }

        categories = response.xpath('//section[contains(@class, "heading pull left")]')
        for category in categories:
            category_name = category.xpath('./h2[@class="label heading pull left"]/@data-title').get()
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
                function_selectors = item.xpath('.//div[contains(@class, "collapsible method item")]')
                for function_selector in function_selectors:
                    function_name = function_selector.xpath('./@data-title').get()
                    function_description = function_selector.xpath('./following-sibling::div[contains(@class, "content")]/p/text()').get()
                    code_parts = function_selector.xpath('./following-sibling::div[contains(@class, "code-container")]//span/text()').extract()
                    code_text = ''.join(code_parts)

                    function_data = {
                        'function_name': function_name,
                        'function_description': function_description,
                        'code_example': code_text,
                    }
                    item_data['functions'].append(function_data)

                category_data['items'].append(item_data)

            data['categories'].append(category_data)

        yield data