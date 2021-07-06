from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import pandas as pd


def ex_money(n):
    n = n.replace(u'\xa0', '')
    if n.startswith('от'):
        money1 = re.findall(r'\d+', n)[0]
        money2 = 0
    elif n.startswith('до'):
        money1 = 0
        money2 = re.findall(r'\d+', n)[0]
    elif n == 'na':
        money1 = 'na'
        money2 = 'na'
    else:
        money1 = re.findall(r'\d+', n.split('-')[0])[0]
        money2 = re.findall(r'\d+', n.split('-')[1])[0]
    return money1, money2


def ex_cur(n):
    if n.endswith('руб.'):
        currency = 'RUR'
    elif n.endswith('EUR'):
        currency = 'EUR'
    elif n == 'na':
        currency = 'na'
    else:
        currency = 'na'
    return currency


def parse_hh(headers, n_pages):
    vacs = []
    for n in range(n_pages):
        main_link = 'https://hh.ru/search/vacancy?st=searchVacancy&text=pandas&page=' + str(n)
        session = requests.Session()
        html = session.get(main_link, headers=headers).text
        parsed_html = bs(html, 'lxml')

        vacancy_list = parsed_html.findAll('div', {'class': 'vacancy-serp-item'})

        for vac in vacancy_list:
            vac_data = {}
            info = vac.find('span', {'class': 'g-user-content'}).findChild()
            money = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
            if not money:
                money = 'na'
            else:
                money = money.getText()
            vac_name = info.getText()
            vac_href = info['href']
            money1, money2 = ex_money(money)

            vac_data['name'] = vac_name
            vac_data['link'] = vac_href
            vac_data['money_1'] = money1
            vac_data['money_2'] = money2
            vac_data['currency'] = ex_cur(money)
            vac_data['source'] = 'HeadHunter'
            vacs.append(vac_data)

        next_page = parsed_html.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if not next_page:
            break
    return vacs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'}

result = parse_hh(headers, 2)

pprint(result)

with open('hh.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
