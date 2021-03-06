from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from scrapy import log 
class AmazonSpider(CrawlSpider):
    name = 'AmazonSpider'
    allowed_domains = ['amazon.cn']
    #start_urls = ['http://associates.amazon.cn/gp/associates/network/main.html']
    start_urls = ['https://associates.amazon.cn/gp/associates/network/reports/report.html']

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.http_user = "yen.chiayi@gmail.com"#username
        self.http_pass = 123123#password
        #login form
        self.formdata = {'create':'0',
                        'email':'yen.chiayi@gmail.com',#self.http_user, 
                        'password':'123123',#self.http_pass,
                        }   
        self.headers = {'ccept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding':'gzip,deflate,sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Cache-Control':'max-age=0',
                        'Connection':'keep-alive',
                        }   
        self.id = 0 

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i},
                                #formdata = self.formdata,
                                headers = self.headers,
                                callback = self.login)#jump to login page

    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))
    def login(self, response):
        self._log_page(response, 'amazon_login.html')
        return [FormRequest.from_response(response, 
                            formdata = self.formdata,
                            headers = self.headers,
                            meta = {'cookiejar':response.meta['cookiejar']},
                            callback = self.parse_item)]#success login

    def parse_item(self, response):
        self._log_page(response, 'after_login.html')

#http://rritw.com/a/bianchengyuyan/C__/20131106/440079.html

