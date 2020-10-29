import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests


url = "https://keithgalli.github.io/web-scraping/challenge/file_1.html"
def get_links_all(links):

    url = 'https://keithgalli.github.io/web-scraping/'
    for link in links:

        url = url + link

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        happens = urllib.request.urlopen(url)
        
        if happens.getcode() =="404":
            print("Not good")
            break
        else:
            
            bodys = soup.find('body')
            print(bodys)

def Scrape_The_Table():
    global r
    global soup

    table = soup.select("table.hockey-stats")[0]
    column = table.find("thead").find_all("th")
    column_names = [c.get_text() for c in column]

    table_rows = table.find("tbody").find_all("tr")
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td]
        l.append(row)

    print("i am here")
    df = pd.DataFrame(l, columns=column_names)
    df.head()
def find_contents(contents):
    new_list = []

    for result in contents:
        if not result.find('a'):
            None
        else:

            strings = result.find_all('a')
            
            values = result['class']
            for find in strings:
                
                d = {
                    "values":find.get_text()
                }

                new_list.append(d)
            
    return new_list

def team_continent(findTd):

    result = findTd.find_all("td")
    contents = find_contents(result)

    return contents

url = 'https://keithgalli.github.io/web-scraping/'
r = requests.get('https://keithgalli.github.io/web-scraping/webpage.html')
soup = BeautifulSoup(r.content, features='html.parser')

#Scrape the links and paragraph
social = soup.find("ul", {"class": "socials"})
paragraph = social.find_all('b')
print(paragraph)

for para in paragraph:

    print(para.get_text())

#Scrape the table

thead = soup.select("table.hockey-stats > thead > tr")
all_th = thead[0].select("th")

for th in all_th:
    print(th['class'])

print("")

table = soup.find("table", {"class": "hockey-stats"})
tbody = table.find("tbody")
tr = tbody.find_all("tr")

for find in tr:
    
    result = team_continent(find)
    break

print(result)

Scrape_The_Table()


#Looking for words
fun_fact = soup.find("ul", {"class": "fun-facts"})
fact = fun_fact.find_all("li", string=re.compile("is"))

print(fact)


#images_div = soup.select("div.row div.column img")
#image_url = images_div[0]['src']
#fetch_url = url + image_url
#img_data = requests.get(fetch_url).content
#with open('lake_como.jpg', 'wb') as handler:
    #handler.write(img_data)

#Get links

get_links = soup.find("div", {"class": "block", "align": "left"})
get_ul = get_links.find('ul')
get_li = get_ul.find_all('li')

all_links = []
for links in get_li:

    all_links.append(links.find('a')['href'])

get_links_all(all_links)








    
    
    
