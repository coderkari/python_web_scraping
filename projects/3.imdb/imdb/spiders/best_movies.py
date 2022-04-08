import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath(
                '//h1[@class="sc-b73cd867-0 fbOhB"]/text()').get(),
            'year': response.xpath(
                '(//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-52284603-1 ifnKcw"])[1]/text()').get(),
            'duration': response.xpath(
                '//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt"]/li[3]/text()').getall(),
            'rating': response.xpath(
                '//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()').get(),
            'genra': response.xpath(
                '//h1[@class="sc-b73cd867-0 fbOhB"]/text()').get(),
            'movie_url': response.url
        }
