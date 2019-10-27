# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru.
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации

from lxml import html
import requests
from pprint import pprint
import datetime
now = datetime.datetime.now()

link1 = 'https://lenta.ru/'
link2 = 'https://mail.ru/'
header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/78.0.3904.70 Chrome/78.0.3904.70 Safari/537.36'}


def replace(n):
    n = n.replace(u'\xa0', '')

months = {'октября': 'October', 'ноября': 'November'}



def news_from_lenta():
    request = requests.get(link1, headers=header)
    root = html.fromstring(request.text)
    news_list = root.xpath('//div[@class="span4"]/div[@class="first-item"] | //div[@class="span4"]/div[@class="item"]')
    news = root.xpath('//div[@class="span4"]/div[@class="item"]/a/text()| //div[@class="span4"]/div[@class="first-item"]/h2/a/text()')
    hrefs = root.xpath('//div[@class="span4"]/div[@class="item"]/a/@href | //div[@class="span4"]/div[@class="first-item"]/a/@href')
    dates = root.xpath('//div[@class="span4"]/div[@class="item"]//time/@datetime | //div[@class="span4"]/div[@class="first-item"]//time/@datetime')

    news_from_lenta = []
    for i in range(len(news_list)):
        data = {}
        data['source'] = link1
        data['news'] = news[i].replace(u'\xa0', ' ')
        data['dates'] = dates[i]
        data['link'] = link1+hrefs[i]
        news_from_lenta.append(data)
    return news_from_lenta

def news_from_mail():
    request = requests.get(link2, headers=header)
    root = html.fromstring(request.text)
    news = root.xpath('//div[contains(@class, "news-item-main")]//h3/text() | //div[contains(@class, "news-item_inline")]//a/text()')
    hrefs = root.xpath('//div[contains(@class, "news-item-main")]//a/@href | //div[contains(@class, "news-item_inline")]//a/@href')
    news_from_mail = []
    for i in range(len(news)):
        data = {}
        data['source'] = link2
        data['news'] = news[i].replace(u'\xa0', ' ')
        data['dates'] = now.strftime("%d-%m-%Y %H:%M")
        data['link'] = link2 + hrefs[i]
        news_from_mail.append(data)
    return news_from_mail

pprint(news_from_lenta())
pprint(news_from_mail())

