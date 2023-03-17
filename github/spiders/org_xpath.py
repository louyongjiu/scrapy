import scrapy

from github.items import GitHubItem


class OrgXpathSpider(scrapy.Spider):
    name = "org-xpath"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/orgs/apache/repositories?language=&q=&sort=stargazers&type=all&page=1"]

    def parse(self, response):
        for node in response.xpath('//*[@id="org-repositories"]/div/div/div[1]/ul/li'):
            item = GitHubItem() 
            item["name"] = str.strip(node.xpath('./div/div[1]/div[1]/h3/a/text()').get())
            item["star"] = str.strip(node.xpath('./div/div[2]/a[2]/text()').getall()[1])
            item["update_time"] = str.strip(node.xpath('./div/div[2]/span/relative-time/@datetime').get())
            item["description"] = str.strip(node.xpath('./div/div[1]/div[1]/p/text()').get() or "")
            yield item

        next_page_url = response.xpath('//*[@id="org-repositories"]/div/div/div[2]/div/a[@class="next_page"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))