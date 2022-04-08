import scrapy


class SpecialProductsSpider(scrapy.Spider):
    name = 'special_products'
    allowed_domains = ['www.cigabuy.com']
    # start_urls = ['https://www.cigabuy.com/specials.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/specials.html', callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'})

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/div"):
            yield{
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'link': product.xpath(".//a[@class='p_box_title']/@href").get(),
                'special_price': product.xpath(
                    ".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'normal_price': product.xpath(
                    ".//div[@class='p_box_price cf']/span[2]/text()").get(),
                'User-Agent': format(response.request.headers['User-Agent'])
            }

            next_page = response.xpath(
                "//a[@class='nextPage']/@href").get()

            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
                })
