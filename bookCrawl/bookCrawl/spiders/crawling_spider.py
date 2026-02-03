from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    # crawling rules
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item")
    )

    # scraping mechanism to do so action adnd get specific
    def parse_item(self, response):
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            # "availability": response.css(".availability::text")[1].get().replace("\n", "").replace(" ", "")
            "availability": response.css(".availability::text").re_first(r"\d+")
        }
        




