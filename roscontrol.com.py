import json

import requests
from bs4 import BeautifulSoup
import lxml

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Accept': '*/*'
}

response = requests.get('https://roscontrol.com/category/produkti/')
src = response.text
# print(src)

soup = BeautifulSoup(src, 'lxml')
all_category_href = soup.find_all(class_="catalog__category-item util-hover-shadow")

product_category_dict = {}
for item in all_category_href:
    category_name = item.find(class_="catalog__category-name").text
    category_href = f'https://roscontrol.com'+item.get('href')

    product_category_dict[category_name] = category_href

    with open('parsing_data/product_category_dict.json', 'w', encoding='utf-8') as file:
        json.dump(product_category_dict, file, indent=4, ensure_ascii=False)


for category_name, category_href in product_category_dict.items():
    response = requests.get(category_href, headers=headers)
    src = response.text
