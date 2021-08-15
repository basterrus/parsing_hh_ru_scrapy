"""2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

"""

import requests
import json

USER_ID = 'Enter your user_id'
TOKEN = 'Enter your token'
""" 
В целях безопасности сделал токен на 1 сутки, не знаю будет ли работать потом, поэтому
лучше ввести свой, ну или просто результат сохранен в файле data_groups.json
"""

URL = f'https://api.vk.com/method/groups.get?user_id={USER_ID}&access_token={TOKEN}&extended=1&v=5.52'
group_data_base = []
req = requests.get(URL).json()

group_data = req['response']['items']

for el in group_data:
    group_data_base.append(f'{el["id"]} -- {el["name"]}')

with open('data_groups.json', 'a', encoding='utf-8') as file:
    json.dump(group_data_base, file, sort_keys=True, indent=4, ensure_ascii=False)

