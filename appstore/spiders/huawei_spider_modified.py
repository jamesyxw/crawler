import scrapy
import re
from scrapy.selector import Selector 
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
    name = "huawei_modified"
    allowed_domains = ["huawei.com"]

    start_urls = [
        "http://appstore.huawei.com/more/all/1"
    ]

    def find_next_page(self, url):
        try:
            page_num_str = url.split('/')[-1]
            page_num = int(page_num_str)+1
            #Limit the number of pages crawl for testing
            if page_num > 1:
                return None

            url = url[:-len(page_num_str)] + str(page_num)
            return url;
        except ValueError:
            print "### next page url cannot be handled"
            print url
            return None

    def parse(self, response):
        page = Selector(response)

        url = response.url

        while url:
            yield scrapy.Request(url, callback=self.parse_page)
            url = self.find_next_page(url)  

    #Parse the current page, go to the main page of each app on the current page
    def parse_page(self, response):
        page = Selector(response)

        #Get the url for every app on the page
        hrefs = page.xpath('//h4[@class="title"]/a/@href')

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)   

    def parse_item(self, response):
        page = Selector(response)
        item = AppstoreItem()

        #Get the item info
        item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()') \
            .extract_first().encode('utf-8')
        item['url'] = response.url
        item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
        item['intro'] = page.xpath('//meta[@name="description"]/@content') \
            .extract_first().encode('utf-8')
        item['thumbnail_url'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first();

        #Collect the recommended app for the current item
        divs = page.xpath('//div[@class="open-info"]')
        recomm = ""
        for div in divs:
            url = div.xpath('./p[@class="name"]/a/@href').extract_first()
            recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
            name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
            recomm += "{0}:{1},".format(recommended_appid, name)
        item['recommended'] = recomm
        yield item
