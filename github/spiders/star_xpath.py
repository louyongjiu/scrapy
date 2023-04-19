import time
import scrapy
from github.items import GitHubItem
from scrapy.downloadermiddlewares.retry import get_retry_request

class StarXpathSpider(scrapy.Spider):
    name = "star-xpath"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/search?o=desc&q=stars%3A10000..13000&s=stars&type=Repositories"]

    def parse(self, response):
        if not response.text:
            yield get_retry_request(
                response.request,
                spider=self,
                reason='empty',
            )
        for node in response.xpath('/html/body/div[1]/div/main/div/div[3]/div/ul/li'):
            item = GitHubItem() 
            item["repository"] = str.strip(node.xpath('./div[2]/div[1]/div[1]/a/text()').get())
            item["star"] = str.strip(node.xpath('./div/div/div/div/a/text()').getall()[1])
            item["update_time"] = str.strip(node.xpath('./div/div/div/div/relative-time/@datetime').get())
            item["name"] = str.strip(node.xpath('./div[2]/div[1]/div[1]/a/text()').get().split('/') [1])
            item["url"] = response.urljoin(node.xpath('./div[2]/div[1]/div[1]/a/@href').get())
            item["description"] = str.strip(node.xpath('./div[2]/p/text()').get() or "")
            yield item

        next_page_url = response.xpath('/html/body/div[1]/div/main/div/div[3]/div/div[2]/div/a[@class="next_page"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
