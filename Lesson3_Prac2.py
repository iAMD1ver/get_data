from pymongo import MongoClient
from pprint import pprint
import json

# 2) Написать функцию, которая производит поиск и выводит
# на экран вакансии с заработной платой больше введенной суммы

client = MongoClient('localhost', 27017)
db = client['BDLESSON3']
jobs = db.jobs



def search(k):
    money = jobs.find({"$or":[{"money_1":{'$ne':'na'}}, {"money_2":{'$ne':'na'}}]})
    for i in money:
        if max(i['money_1'], i['money_2']) >= k:
            pprint(i)

search(int(input('Введите минимальную желаемую зарплату: ')))