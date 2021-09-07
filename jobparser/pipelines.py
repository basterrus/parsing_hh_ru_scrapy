from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_sal'], item['max_sal'], item['currency'] = self.process_salary_hh(item['salary'])
        else:
            item['min_sal'], item['max_sal'], item['currency'] = self.process_salary_hh(item['salary'])
            item['salary'] = ''.join(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        try:
            salary = salary.replace('\u202f', '')
            salary = salary.replace('\xa0', '')
            if 'до' in salary and 'от' in salary:
                min_sal = float([symb for symb in salary.split(' ')][1])
                max_sal = float([symb for symb in salary.split(' ')][3])
                currency = [symb for symb in salary.split(' ')][4]
            elif 'от ' in salary:
                min_sal = float([symb for symb in salary.split(' ')][1])
                max_sal = None
                currency = [symb for symb in salary.split(' ')][2]
            elif 'до ' in salary:
                min_sal = None
                max_sal = float([symb for symb in salary.split(' ')][1])
                currency = [symb for symb in salary.split(' ')][2]
            else:
                min_sal = None
                max_sal = None
                currency = None
        except:
            min_sal = None
            max_sal = None
            currency = None

        return min_sal, max_sal, currency

    def process_salary_sj(self, salary):
        if salary == [''] or salary == ['По договорённости'] or salary == []:
            currency = None
            min_sal = None
            max_sal = None
        else:
            currency = 'руб.'
            min_sal = None
            max_sal = None
            for elem in range(len(salary)):
                salary[elem] = salary[elem].replace('\xa0', '')
            if '—' in salary:
                min_sal = int(salary[0])
                max_sal = int(salary[4])
            elif 'от' in salary:
                salary_dict = []
                for item in salary[2]:
                    if item.isdigit():
                        salary_dict.append(item)
                min_sal = int(''.join(salary_dict))
            elif 'до' in salary:
                salary_dict = []
                for item in salary[2]:
                    if item.isdigit():
                        salary_dict.append(item)
                max_sal = int(''.join(salary_dict))
        return min_sal, max_sal, currency
