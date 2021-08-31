import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import lxml
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Accept': '*/*'
}

area_dict = {
    'россия': 113,
    'москва': 1,
    'санкт петербург': 2,
}


def main():
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh']
    vacancy = db.vacancy

    vacancy_name = input('Введите название вакансии: ').lower()
    vacancy_area = input('Введите регион поиска: ').lower()
    if vacancy_area in area_dict:
        vacancy_area = area_dict[vacancy_area]

    else:
        print('Введите правильное значение!')

    page = 0
    while True:

        url = f'https://hh.ru/search/vacancy?area={vacancy_area}&text={vacancy_name}&page={page}'

        response = requests.get(url=url, headers=headers)
        src = response.text

        soup = BeautifulSoup(src, 'lxml')
        all_vacancy_info = soup.find_all('div', {'class': 'vacancy-serp-item'})

        # vacancy_list = []
        vacancy_list = {}
        for vacancy in all_vacancy_info:
            vacancy_card = vacancy.find('a')
            vacancy_name = vacancy_card.text
            vacancy_href = vacancy_card.get('href')

            try:
                sal_info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                sal_cur = sal_info[-1]

                if sal_info[0] == 'от':
                    sal_min = int(sal_info[1].replace(u'\u202f', ''))
                    sal_max = None
                elif sal_info[0] == 'до':
                    sal_min = None
                    sal_max = int(sal_info[1]).replace(u'\u202f', '')
                else:
                    sal_min = sal_info[0].replace(u'\u202f', '')
                    sal_max = sal_info[2].replace(u'\u202f', '')
            except:
                sal_min = None
                sal_max = None
                sal_cur = None

            # vacancy_list.append({
            #     'Название вакансии': vacancy_name,
            #     'Ссылка на вакансию': vacancy_href,
            #     'Минимальная зарплата': sal_min,
            #     'Максимальная зарплата': sal_max,
            #     'Валюта': sal_cur,
            # })

            vacancy_list['vacancy_name'] = vacancy_name
            vacancy_list['vacancy_href'] = vacancy_href
            vacancy_list['sal_min'] = sal_min
            vacancy_list['sal_max'] = sal_max
            vacancy_list['sal_cur'] = sal_cur

            with open('vacancy_data.json', "a", encoding="utf-8") as file:
                json.dump(vacancy_list, file, indent=4, ensure_ascii=False)

        print(f'Сохранены данные страницы {page}')
        page += 1

        if not soup.find(text='дальше'):
            try:
                break
            except AttributeError:
                print('Больше нет страниц для перебора!')

    vacancy.update_many(vacancy_list)

# ХОТЬ ТРЕСНИ НЕ ПОНИМАЮ ПОЧЕМУ ОШИБКА НОН ТАЙП


if __name__ == '__main__':
    main()
