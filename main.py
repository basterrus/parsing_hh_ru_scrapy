import requests
from bs4 import BeautifulSoup
import lxml

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Accept': '*/*'
}

area_dict = {
    'россия': 113,
    'москва': 1,
    'санкт петербург': 2,
}


def main():
    global url
    vacancy_name = 'курьер'  # input('Введите название вакансии: ').lower()
    vacancy_area = 'москва'  # input('Введите регион поиска: ').lower()
    if vacancy_area in area_dict:
        vacancy_area = area_dict[vacancy_area]
        url = f'https://hh.ru/search/vacancy?area={vacancy_area}&text={vacancy_name}'
    else:
        print('Введите правильное значение!')

    response = requests.get(url=url, headers=headers)
    src = response.text

    soup = BeautifulSoup(src, 'lxml')
    all_vacancy = soup.find_all('div', {'class': 'vacancy-serp-item'})
    print(all_vacancy)


if __name__ == '__main__':
    main()
