from http import cookiejar
from scrapy import Request
from uuid import uuid4
import scrapy
from scrapy import FormRequest
from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import re
from pymongo import MongoClient

try:
    import pytesseract
except ImportError:
    print('pytesseract not found')

class karnataka_data(scrapy.Spider):
    name="district_name"
    
    def start_requests(self):
        yield Request('https://ceo.karnataka.gov.in/finalroll_2022/Dist_List.aspx',
            meta={'cookiejar':str(uuid4())},
            callback=self.parse) 
    
    def parse(self,response):
        district_table=response.xpath('//*[@id="ContentPlaceHolder1_GridView1"]//tr//td[2]/font/a/@href').extract()
    
        for no in district_table:
            yield Request('https://ceo.karnataka.gov.in/finalroll_2022/{}'.format(no),
                meta={'cookiejar':response.meta["cookiejar"],'district_code':no.split('=')[1:]},
                callback=self.AC_No)
                  
    def AC_No(self,response):
        Ac_no_table=response.xpath('//*[@id="ContentPlaceHolder1_GridView1"]//tr/td/font/a/@href').extract()
         
        for Ac_no in Ac_no_table:
            yield Request('https://ceo.karnataka.gov.in/finalroll_2022/{}'.format(Ac_no),
                meta={'cookiejar':response.meta["cookiejar"],'district_code':response.meta['district_code'],
                      'ac_no':Ac_no},
                callback=self.MR_No)
            
    def MR_No(self,response):
        Mr_no_table=response.xpath('//*[@id="ContentPlaceHolder1_GridView1"]//tr/td[4]/font/a/@href').extract()
        for Mr_no in Mr_no_table:
            datas=Mr_no.strip('CodeCaputer1.aspx?field1=.%2f')
            no=datas.split('&')
            data=no[0]
            yield Request('https://ceo.karnataka.gov.in/finalroll_2022/{}'.format(data),
                meta={'cookiejar':response.meta["cookiejar"],'district_code':response.meta['district_code'],'ac_no':response.meta['ac_no'],'mr_no':Mr_no},
                callback=self.pdf)
    
    def pdf(self,response):
        file_name = "{}{}{}".format(response.meta['district_code'][0],response.meta['ac_no'].split('=')[1],response.meta['mr_no'].split('=')[3])
        with open('{}.pdf'.format(file_name),'wb') as f:
            f.write(response.body)
        
        PDF_file = '{}.pdf'.format(file_name)
        pages=convert_from_path(PDF_file,150)
        image_counter=1
        for page in pages:
            filename="page_"+str(image_counter)+".jpg"
            page.save(filename,'JPEG')
            image_counter+=1
        filelimit=image_counter-1
        outfile="out_text.txt"
        f=open(outfile,"a")
        data_=[]
        for i in range(3,filelimit):
           
            filename = "page_"+str(i)+".jpg" 
            text=str(((pytesseract.image_to_string(Image.open(filename)))))
            epic_no=re.findall("[A-Z]{3}[0-9]{7}",text)
            text=text.replace('-\n','') 
            f.write(text)  
            data_.extend(epic_no)
        mongo_data=self.mongo_connect('karnataka_epic_no')
        mongo_data.insert_one({'epic_data':data_})

    def mongo_connect(self,collection_name):
        connection = MongoClient("mongodb://scraperDev:0mtNHqMELizgmHkp@dev-mongo-db.advarisk.com:27711/?")
        collection = connection['Land_Records'][collection_name]
        return collection   