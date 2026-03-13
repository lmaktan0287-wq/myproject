import scrapy

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Scraping quotes and authors
        quotes = response.css('span.text::text').getall()
        authors = response.css('small.author::text').getall()

        for i in range(len(quotes)):
            yield {
                'quote': quotes[i],
                'author': authors[i]
            }

        # Go to next page automatically
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)