from pymongo import MongoClient
from pprint import pprint
import json
import time


# 3*)Написать функцию, которая будет добавлять в вашу
# базу данных только новые вакансии с сайта.


client = MongoClient('localhost', 27017)
# client.drop_database('BDLESSON3')
db = client['BDLESSON3']
jobs = db.jobs

# функция представляет собой модификацию функции, представленной в задании 1
# проверка при загрузке вакансий в базу происходит методом простого перебора по контрольным значениям.
# в качестве контрольных значений выступает комбинация полей: `name` и `link`

def load_data(n):
    with open(n + '.json', 'r', encoding='utf-8') as f:
        n = json.load(f)
    for i in n:
        if i['money_1'] != 'na':
            i['money_1'] = int(i['money_1'])
        if i['money_2'] != 'na':
            i['money_2'] = int(i['money_2'])

    coursor = list(jobs.find())
    count_match = 0
    count_new = 0
    count_overall = 0
    for item in n:
        check = str(item['link']).split('?')[0] + ' ' + str(item['name'])
        count_overall += 1
        for obj in coursor:
            check_obj = str(obj['link']).split('?')[0] + ' ' + str(obj['name'])
            if check_obj == check:
                count_match += 1
                break
        else:
            jobs.insert_one(item)
            count_new += 1
    print('')
    print('источник загрузки: {}'.format(item['source']))
    print('всего загружалось вакансий: {}'.format(count_overall))
    print('совпало вакансий: {}'.format(count_match))
    print('добавлено вакансий: {}'.format(count_new))
    print('-------------------------------')



load_data('hh')
load_data('sj')
