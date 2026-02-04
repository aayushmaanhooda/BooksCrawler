# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''
What is ItemAdapter
It's a wrapper that lets you treat different item types the same way.
Your item could be:

A dict
A Scrapy Item
A Pydantic model

ItemAdapter doesn't care. It gives you a consistent way to access fields.
pythonadapter = ItemAdapter(item)
# Now you can use adapter.get(), adapter.field_names() 
# regardless of whether item is dict, Item, or Pydantic

'''

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class BookcrawltwoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        # strip all whitesapces from strings
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = value.strip()


        # category & Product ttype --> switch to lowercase
        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)
            
        # get only number from availability
        availabilty_string = adapter.get("availability")
        numbers = re.search(r'\d+', availabilty_string)
        adapter["availability"] = numbers.group()

        return item
