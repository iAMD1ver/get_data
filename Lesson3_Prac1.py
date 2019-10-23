from pymongo import MongoClient
from pprint import pprint
import json

# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД

client = MongoClient('localhost', 27017)
client.drop_database('BDLESSON3')
db = client['BDLESSON3']
jobs = db.jobs


def load_data(n):
    with open(n + '.json', 'r', encoding='utf-8') as f:
        n = json.load(f)
    for i in n:
        if i['money_1'] != 'na':
            i['money_1'] = int(i['money_1'])
        if i['money_2'] != 'na':
            i['money_2'] = int(i['money_2'])
    jobs.insert_many(n)


load_data('hh')
load_data('sj')
