from scrapy import Spider
from scrapy.selector import Selector
from items import StockScraperItem as Item
from scrapy.crawler import CrawlerProcess
import os, time
# import sched, time
# s = sched.scheduler(time.time, time.sleep)
class StockScraper(Spider):
    name = 'StockScraper'
    allowed_domains = ["merolagani.com"]
    start_urls = [
        "https://merolagani.com/LatestMarket.aspx"
    ]
    def parse(self, response):
        stocks = Selector(response).xpath(f'//*[@id="ctl00_ContentPlaceHolder1_LiveTrading"]/table/tbody/tr')
        for stock in stocks:
            item = Item()
            item['company_name'] = stock.xpath('td//text()')[0].extract()
            item['LTP'] = stock.xpath('td//text()')[1].extract()
            item['change'] = stock.xpath('td//text()')[2].extract() 
            yield item


def process_initializer():
    process = CrawlerProcess(settings = {
    "FEEDS":{
        "items.json" : {"format":"json"}
    }
})

    os.remove("items.json")
    process.crawl(StockScraper)
    process.start()


def app(interval = 5):
    process_initializer()
    while True:
        time.sleep(interval)
        os.system("python stock_scraper.py")

app()