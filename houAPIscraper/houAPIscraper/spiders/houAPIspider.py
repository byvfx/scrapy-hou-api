import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HouAPIspider(CrawlSpider):
    name = "houAPI"
    allowed_domains = ["sidefx.com"]
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/index.html"]

    rules = (
        Rule(LinkExtractor(allow=(r'/docs/houdini/hom/hou/')), callback='parse_item'),

    )

    def parse_item(self, response):
    # Extract the category text and strip whitespace
        logging.info(f"Scraping URL: {response.url}")
        category_text = response.css('h2.label.heading.pull.left::text').get().strip()

        if category_text:
            category_text = category_text.strip()
            yield {'category': category_text}
        else:
            logging.info(f"No category found for URL: {response.url}")

    
            
