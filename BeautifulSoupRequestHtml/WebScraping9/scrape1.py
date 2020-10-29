import requests
from bs4 import BeautifulSoup

#Define a base url
BASE_URL = 'https://www.yellow-pages.ph/search/coffee/nationwide/page-1'

r = requests.get(BASE_URL)
soup = BeautifulSoup(r.content, 'html.parser')

for link in soup.find_all("a"):

        try:
            if "https" in link['href']:
                print(link['href'])
                print(link.get_text())
        except KeyError:

            print("Does Not Contain HREF")

general_data = soup.find_all("div", {"class": "search-listing"})

for data in general_data:

   business = data.find("div", {"class":"search-business-otherinfo"}).text.strip()
   print(business)
   