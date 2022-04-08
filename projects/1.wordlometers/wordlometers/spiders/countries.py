import logging
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    # country_name = ''
    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
            # self.country_name = name
            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})
            # yield{
            #     'country': self.country_name,
            #     'link': link
            # }

    def parse_country(self, response):
        logging.info(response.url)

        populations = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for population in populations:
            year = population.xpath(".//td[1]/text()").get()
            people = population.xpath(".//td[2]/strong/text()").get()
            name = response.request.meta['country_name']
            yield{
                "country": name,
                "people": people,
                "year": year
            }
