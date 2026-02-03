import scrapy
from newsCrawl.items import NewscrawlerItem
from urllib.parse import urljoin

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["nbcnews.com"]
    start_urls = [
        "https://www.nbcnews.com"
    ]

    def parse(self, response):
        headlines = response.css('article a, .headline a, h2 a, h3 a')
        seen_links = set()

        for headline in headlines:
            item = NewscrawlerItem()

            link = headline.css("::attr(href)").get()

            if link:
                link = urljoin(response.url, link)
            
                if link in seen_links:
                    continue
                seen_links.add(link)
            
            title = headline.css("span::text").get()
            if not title:
                title = headline.css("::text").get()
            
            if title and link and 'nbcnews.com' in link:
                item["title"] = title.strip()
                item["link"] = link
                item["source"] = "NBC News"

        yield scrapy.Request(
                    link,
                    callback=self.parse_article,
                    meta = {
                        "item": item
                    }
                )

    def parse_article(self, response):
        item = response.meta["item"]
        date =  response.css("time::attr(datetime)").get()

        if not date:
            date = response.css("time::text").get()

        summary = response.css("p.lede::text, .article-body p:first-child::text").get()

        if not summary:
            summary = response.css("article p::text").get()


        if date and summary:
            item["date"] = date.strip()
            item["summary"] = summary.strip()

        yield item