from scrapy import Request
from pymongo import MongoClient
import scrapy

class karnataka_data(scrapy.Spider):
    name="industry_name"
    
    def start_requests(self):
        yield Request('https://www.bseindia.com/corporates/List_Scrips.html',
            callback=self.parse) 
    
    def parse(self,response):
        import pdb;pdb.set_trace()
        industry_table=response.xpath('//*[@id="ddlIndustry"]/option/@value').extract()
        print(industry_table,'**************************************')
        