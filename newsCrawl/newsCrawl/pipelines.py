# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewscrawlPipeline:
    def process_item(self, item, spider):

        adaptor = ItemAdapter(item)

        if adaptor.get("title"):
            adaptor["title"] = " ".join(adaptor["title"].split())

        if adaptor.get("link") and not adaptor["link"].startswith("http"):
            adaptor["link"] = spider.starts_url[0] + adaptor["link"]


        if adaptor.get("summary"):
            adaptor["summary"] =" ".join(adaptor["summary"].split())



        return item
