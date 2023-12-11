import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    custom_settings = {'CLOSESPIDER_TIMEOUT': 30}
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/index.html"]

    rules = (
        Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_start_url',follow=True),
        Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_detail_page'),
    )

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
            category_data = {
                'category': category_name,
                'items': []
            }

            items = category.xpath('.//li[contains(@class, "subtopics_item")]')
            for item in items:
                item_title = item.xpath('./p[@class="label"]/a/text()').get()
                item_summary = item.xpath('./p[@class="summary"]/text()').get()
                detail_page_url = item.xpath('./p[@class="label"]/a/@href').get()

                if detail_page_url:
                    yield response.follow(detail_page_url, callback=self.parse_detail_page, meta={'item_title': item_title, 'item_summary': item_summary, 'category_data': category_data})

            data['categories'].append(category_data)

        yield data

    def parse_detail_page(self, response):
        item_title = response.meta['item_title']
        item_summary = response.meta['item_summary']
        category_data = response.meta['category_data']

        function_names = response.css('div.collapsible.method.item.collapsed::attr(data-title)').getall()

        item_data = {
            'class': item_title,
            'summary': item_summary,
            'functions': function_names,
        }
        category_data['items'].append(item_data)

        # Assuming you handle the final data aggregation here or in some other way
