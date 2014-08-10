from dragline.htmlparser import HtmlParser
from dragline.http import Request
from urllib import urlretrieve

class Spider:

    def __init__(self, conf):
        self.name = "natgeo"
        self.start = "http://photography.nationalgeographic.com/photography/wallpapers"
        self.allowed_domains = ['photography.nationalgeographic.com']
        self.conf = conf

    def parse(self,response):
        html = HtmlParser(response)
        photo_list = ['//li[@class="first"]','//li[@class=" "]','//li[@class="last"]']
        for item in photo_list:
	    for url in html.extract_urls(item):
	        yield Request(url,callback="parseAnimals")
	    
	    
    def parseAnimals(self,response):
        html = HtmlParser(response)
        if html.extract_urls('//div[@class="pagination"]/a[@class="next"]'):
	    for url in html.extract_urls('//div[@id="search_results"]/div/a'):
		yield Request(url,callback="parseAnimal")
	    for url in html.extract_urls('//div[@class="pagination"]/a[@class="next"]'):
		yield Request(url,callback="parseAnimals")
        else:
	    for url in html.extract_urls('//div[@id="search_results"]/div/a'):
		yield Request(url,callback="parseAnimal")
		
    def parseAnimal(self,response):
        print 'parseAniml'
        html = HtmlParser(response)
        print 'Downloading........'
        for url in html.xpath('//div[@class="primary_photo"]/a/img/@src'):
	    urlretrieve(url,url.split('/')[-1])