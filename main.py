from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['lenta_news']
news = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get('https://lenta.ru/parts/news/', headers=header)
dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@data-more-url,'/parts/news')]")

for el in items:
    info_card = {}
    category = el.xpath("./div/a/text()")
    name = el.xpath("./div/h3/a/text()")
    href = el.xpath("./div/h3/a/@href")
    time_date = el.xpath("./div/text()")

    info_card['category'] = category
    info_card['href'] = href
    info_card['time_date'] = time_date
    info_card['name'] = name

    news.insert_one(info_card)

