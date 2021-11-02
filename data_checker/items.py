# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Dataset(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    organization = scrapy.Field()
