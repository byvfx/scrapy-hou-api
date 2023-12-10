import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    custom_settings = {'CLOSESPIDER_TIMEOUT': 60}
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
        print(f"Processing URL: {response.url}")  # Print the current URL being processed
        data = {
            'title': 'hou package',
            'categories': []
        }

        categories = response.xpath('//section[contains(@class, "heading pull left")]')
        for category in categories:
            category_name = category.xpath('./h2[@class="label heading pull left"]/@data-title').get()
            print(f"Category Name: {category_name}")  # Print the category name
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

                # Extract function names
                function_names = response.css('div.collapsible.method.item.collapsed::attr(data-title)').getall()

                for function_name in function_names:
                    # Placeholder for function description and code
                    function_description = ' '.join(response.xpath('//*[@id="brief"]/div/p/text()').extract())
                    code_text = ''  # Adjust this to extract the correct code

                    function_data = {
                        'function_name': function_name,
                        'function_description': function_description,
                        'code_example': code_text,
                    }
                    item_data['functions'].append(function_data)

                    category_data['items'].append(item_data)

            data['categories'].append(category_data)

        yield data
