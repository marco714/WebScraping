import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

list_property = []
def pagination(page):

    global list_property
    url = f'https://www.holidayfrancedirect.co.uk/search?board=sc&people=2&page={page}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    content = soup.find_all('div', {"class": "property-grid-item"})

    
    for property in content:

        name = property.find('h2').text
        rating = property.find('p').text
        price = property.find('div', {"class": "property-pricing"}).text

        property_info = {
            "Name": name,
            "Rating": rating,
            "Price": price
        }

        list_property.append(property_info)

    
    print(len(list_property))
    time.sleep(3)



for i in range(1, 3):

    pagination(i)

df = pd.DataFrame(list_property)

#Print first five Lines
print(df.head())

df.to_csv('holidayhomes.csv')
#print(soup.title)