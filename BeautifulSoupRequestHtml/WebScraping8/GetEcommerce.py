import requests
from bs4 import BeautifulSoup
import pandas as pd

BASEURL = 'https://www.thewhiskyexchange.com/'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

productLinks = []
for x in range(1, 6):
    r = requests.get(f'https://www.thewhiskyexchange.com/search?q=whiskey&pg={x}#productlist-filter')
    soup = BeautifulSoup(r.content, 'html.parser')

    productList = soup.find_all('div', {"class": "item"})
    

    for item in productList:

        for link in item.find_all('a', href=True):
            productLinks.append(BASEURL + link['href'])


#testLink = 'https://www.thewhiskyexchange.com/p/33402/whisky-thief-bourbon-3-year-old'

whiskey_links = []
for link in productLinks:
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find('h1', {"class": "product-main__name"}).text.split("\n")[1]
    price = soup.find('p', {"class": "product-action__price"}).text[1:].strip()

    try:
        rating = soup.find('div', {"class": "review-overview"}).text.strip()
    except:
        rating = 'No Rating'

    whiskey = {
        'name':name,
        'rating': rating,
        'price': price
    }

    whiskey_links.append(whiskey)
    print(f'Saving: {whiskey}')

df = pd.DataFrame(whiskey_links)
print(df.head(15))
