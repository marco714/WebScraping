import requests
from bs4 import BeautifulSoup


def pagination(page):
    url = f'http://books.toscrape.com/catalogue/page-{page}.html'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    article = soup.find_all('article', {"class": "product_pod"})
    book_list = []

    for book in article:
        
        title = book.find_all('a')[1]['title']
        price = book.find('p', {"class": "price_color"}).text[2:]
        instock = book.find('p', {"class": "instock availability"}).text.strip()

        books = {
            'title':title,
            'price':price,
            'instock': instock
        }

        book_list.append(books)

    print(book_list)


for i in range(1, 3):

    pagination(i)
