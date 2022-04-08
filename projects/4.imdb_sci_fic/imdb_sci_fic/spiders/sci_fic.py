import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SciFicSpider(CrawlSpider):
    name = 'sci_fic'
    allowed_domains = ['www.imdb.com']
    # start_urls = [
    #     'https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&view=simple']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&view=simple', headers={'User_Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//span[@class="lister-item-header"]//a'),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[2]'),
             follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        return {
            'title': response.xpath(
                "//h1[@class='sc-b73cd867-0 eKrKux']/text()").get(),
            'year': response.xpath(
                "(//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-52284603-1 ifnKcw'])[1]/text()").get(),
            'duration': response.xpath(
                "//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt']/li[@class='ipc-inline-list__item'][last()]/text()").getall(),
            'rating': response.xpath(
                "(//span[@class='sc-7ab21ed2-1 jGRxWM'])[1]/text()").get(),
            'url': response.url,
            'user_agent': response.request.headers['User-Agent']
        }
