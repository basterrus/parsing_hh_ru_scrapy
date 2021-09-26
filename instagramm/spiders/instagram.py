import scrapy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 89998893770
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1631814147:AfVQAKYM+8Lf/DtVrQuXTFlq6beJbOA6mKWSwA13GQnawgFO+84fuhgDGATyApOUv0eNp4D8wRknxKglxTOjJQJ475Oqyx9pfiKf7gLBMWakKB/sCSHFRkQ9dN26FLO60LsaWf7Gk1gH6ocnmA=='

    def parse(self, response: HttpResponse):
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': 'inst_login', }
        )

    def login(self, response: HttpResponse):
        print()

