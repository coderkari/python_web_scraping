import scrapy
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formname="register",
            formdata={
                'username': 'karimul483@gmail.com',
                'password': '/bf82Z*r_wDJR*j',
                'redirect': '/account/loans',
                'debug_token': '',
                'login': 'Log In'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        print('log in')
