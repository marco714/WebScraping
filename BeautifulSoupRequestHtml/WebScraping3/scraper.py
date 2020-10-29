import requests
from bs4 import BeautifulSoup
import smtplib as sntgmail

URL = 'https://www.amazon.com/Newest-Sony-Playstation-Gaming-Console/dp/B0825526SW/ref=sr_1_5?dchild=1&keywords=ps4&qid=1596086784&sr=8-5'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


def check_price():

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')


    title = soup.find('span', id="productTitle").get_text().strip()
    price = soup.find('span', id="priceblock_ourprice").get_text()
    converted_price = float(price[1:4])

    if converted_price < 1000:
        send_mail()


    print(converted_price)
    print(title)

def send_mail():
    
    server = sntgmail.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('narcamarco@gmail.com', 'lordgrim18')

    subject = 'Price Fell Down! '
    body = 'Check The amazon Link https://www.amazon.com/Newest-Sony-Playstation-Gaming-Console/dp/B0825526SW/ref=sr_1_5?dchild=1&keywords=ps4&qid=1596086784&sr=8-5' 

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'narcamarco@gmail.com',
        'narcamarco@gmail.com',
        msg
    )

    print('Hey Email has been sent')
    server.quit()

check_price()