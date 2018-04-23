import scrapy


class BBCNewsSpider(scrapy.Spider):
    name = "bbcnews"
    start_urls = [
        "http://www.bbc.com/news",
    ]

    def parse(self, response):
        print(response.css("title::text").extract_first())