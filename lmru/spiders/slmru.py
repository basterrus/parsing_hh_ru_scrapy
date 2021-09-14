import scrapy
from scrapy.http import HtmlResponse
from lmru.items import LmruItem
from scrapy.loader import ItemLoader


class SlmruSpider(scrapy.Spider):
    name = 'slmru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/nabory-instrumentov/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]/@href').getall()
        next_page = response.xpath(
            '//a[@class="bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(response=response, item=LmruItem())
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('description', '//div/p/text()')
        # loader.add_xpath('spec', '//div[@class="def-list__group"]//text()')
        loader.add_xpath('images', '//img[@slot="thumbs"]/@src')
        yield loader.load_item()
        # print()





        # name = response.xpath('//h1/text()').get()
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # link = response.url
        # description = response.xpath('//div/p/text()').get()
        # characteristic_key = response.xpath('//dt[@class="def-list__term"]/text()').getall()
        # characteristic_value = response.xpath('//dd[@class="def-list__definition"]/text()').getall()
        # images = response.xpath('//img[@slot="thumbs"]/@src')
        # yield LmruItem(name=name, price=price, link=link, description=description,
        #                characteristic_key=characteristic_key, characteristic_value=characteristic_value, images=images)

