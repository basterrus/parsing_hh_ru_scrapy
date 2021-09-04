from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

# Подключаем MongoDB
connect = MongoClient('localhost', 27017)
db = connect.mvideo
collect = db.mvideo_collect

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./web/chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

# Ищем блок Новинки и листаем на него
position = driver.find_element_by_xpath("//body/div[2]/div[1]/div[3]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/a[2]")
position.send_keys(Keys.PAGE_DOWN)

# Ищем кнопку пролистывания вправо и прогружаем все товары новинок
button = driver.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[7]/div[1]/div[2]/div[1]/div[1]/a[2]')
while 'disabled' not in button.get_attribute('class'):
    button.click()

goods_item = driver.find_elements_by_xpath(
    '//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/li[@class = '
    '"gallery-list-item"]')

for elem in goods_item:
    goods_dict = {}

    # goods_name = elem.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[4]/div[1]/div[2]/div[1]/div['
    #                                            '1]/div[1]/ul[1]/li[1]/div[1]/div[3]/div[1]/div[1]/h3[1]')
    # goods_price = elem.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[4]/div[1]/div[2]/div[1]/div['
    #                                             '1]/div[1]/ul[1]/li[1]/div[1]/div[5]/div[1]/div[1]/span[1]')
    goods_rating = elem.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[4]/div[1]/div[2]/div[1]/div['
                                                 '1]/div[1]/ul[1]/li[1]/div[1]/div[3]/div[1]/div[1]/div[1]/a[1]/div['
                                                 '1]/span[2]')
    # goods_href = elem.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[4]/div[1]/div[2]/div[1]/div['
    #                                                '1]/div[1]/ul[1]/li[1]/div[1]/div[3]/div[1]/div[1]/div[1]/a['
    #                                                '1]').get_attribute('href')

    goods_name = elem.find_element_by_tag_name('a').get_attribute('data-track-label')
    goods_href = elem.find_element_by_tag_name('a').get_attribute('href')
    goods_price = elem.find_element_by_xpath('//body/div[2]/div[1]/div[3]/div[1]/div[7]/div[1]/div[2]/div[1]/div['
                                             '1]/div[1]/ul[1]/li[1]/div[1]/div[5]/div[1]/div[1]/span[1]')

    goods_dict['Товар'] = goods_name
    goods_dict['Цена'] = goods_price.text.replace(' ', '')
    goods_dict['Рейтинг'] = goods_rating.text
    goods_dict['Ссылка'] = goods_href

    collect.update_one({'url': goods_href}, {'$set': goods_dict}, upsert=True)

driver.close()


