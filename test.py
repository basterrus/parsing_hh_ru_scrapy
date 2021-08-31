from pymongo import MongoClient
import pprint


client = MongoClient('localhost', 27017)

db = client['hh']

mycol = db.vacancy

user_data  = {
    'name': 'Кура',
    'year': 120,
}


mycol.insert_one(user_data)


for i in mycol.find({}):
    print(i)

