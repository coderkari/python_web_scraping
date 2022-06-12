import scrapy
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'karimul',
                'password': 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        logout_button = response.xpath("//a[@href='/logout']/text()").get()
        if logout_button:
            print('log in')
