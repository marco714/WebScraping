import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
def real_time_price(stock_code):

    url = ('https://finance.yahoo.com/quote/') + stock_code + ('.HK?p=') + stock_code + ('.HK&.tsrc=fin-srch')
    r = requests.get(url)
    web_content = BeautifulSoup(r.content, 'html.parser')

    web_content = web_content.find('div', {"class": 'My(6px) Pos(r) smartphone_Mt(6px)'})

    web_content = web_content.find('span').text

    if web_content == []:
        web_content = '99999'

    return web_content

HSI = ['0001', '0002', '0003', '0005']


for step in range(1,101):
    price = []
    col = []
    time = datetime.datetime.now()
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")

    for stock_price in HSI:

        price.append(real_time_price(stock_price))

    col = [time_stamp]
    col.extend(price)

    df = pd.DataFrame(col)
    df = df.T
    df.to_csv('realTimeStockData.csv', mode='a', header=False)
    print(col)
