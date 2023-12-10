import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/index.html"]

    rules = (
        Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou')), callback='parse_item'),

    )

    def parse_item(self, response):
        
        yield {
            'category': response.css('h2.label.heading.pull.left::attr(data-title)').get(),
            #'homclass': response.css('a.label-text.homclass::text').get(),
            # 'summary': response.css('p.summary::text').getall(),
        }