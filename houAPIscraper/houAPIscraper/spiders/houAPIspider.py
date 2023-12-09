import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/"]

    rules = (
        Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_item', follow=True),

    )

    def parse_item(self, response):
        pass
    
            
