import scrapy
import scrapy


class HouAPIspider(scrapy.Spider):
    name = "houAPI"
    start_urls = ["https://www.sidefx.com/docs/houdini/hom/hou/"]

    def parse(self, response):
        for cats in response.css('div.content'):
            name = cats.css('a.label-text.homclass::text').get()
            summary = cats.css('p.summary::text').get(default='none')
            link = cats.css('a.label-text.homclass::attr(href)').get(default='none')

            yield {
                "name": name,
                "summary": summary,
                "link": link,
            }
