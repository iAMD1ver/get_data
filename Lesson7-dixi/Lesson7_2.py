from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
from pymongo import MongoClient


driver = webdriver.Firefox(executable_path="/home/dmitrii/Documents/Python/Get_data/Lesson7/geckodriver")
driver.get('https://dixy.ru/catalog/')

client = MongoClient('localhost', 27017)
db = client['BDLESSON7_2']
dixi = db.dixi

pages = 1
while True:
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'view-more')))
        button.click()
        pages +=1
        print(f'Открыта {pages} старница')
    except Exception as e:
        print(e)
        break

parse = driver.page_source
root = html.fromstring(parse)


products = root.xpath("//div[contains(@class, 'item ')]//div[contains(@class, 'product-main')]/*/@alt")
price = root.xpath("//p[@itemprop='price']/@content")

products_dixi = []

for i in range(len(products)):
    data = {}
    data['products'] = products[i]
    data['price'] = price[i]
    print(data)
    dixi.insert_one(data)



