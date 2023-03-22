# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GitHubItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    star = scrapy.Field()
    update_time = scrapy.Field()
    description = scrapy.Field()
    repository = scrapy.Field()
    url = scrapy.Field()
