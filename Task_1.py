"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.

"""
import requests
import json

USERNAME = 'basterrus'  # Ввести свой логин на GitHub
TOKEN = 'enter your token'  # Ввести свой токен авторизации для GitHub
URL = 'https://api.github.com/user/repos'

data_repo = []
connect = requests.get(URL, auth=(USERNAME, TOKEN))  # Отправляем Get запрос с данными авторизации
for el in connect.json():
    data_repo.append(f"{el['name']} : {el['url']}")

with open('data.json', 'a', encoding='utf-8') as file:  # Сохранение данных в json файл
    json.dump(data_repo, file, sort_keys=True, indent=4, ensure_ascii=False)
