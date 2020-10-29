import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://keithgalli.github.io/web-scraping/example.html')
soup = BeautifulSoup(r.content, features='html.parser')

firstHeader = soup.find("h2")
headers = soup.find_all("h2")

print(headers[0].get_text())
print(firstHeader)

print("")
# Dependes on what it is being found first
secondHeader = soup.find(["h1", "h2"])
print(secondHeader)

print("")
allHeaders = soup.find_all(["h1", "h2"])
print(allHeaders)

print("")
#Pass the attribute to the find/ find_all function
paragraph = soup.find_all("p", attrs={"id": "paragraph-id"})
print(paragraph)

print("")
#Nest find/find_all 
body = soup.find('body')
div = body.find('div')
print(div)

print("")
#Search specific strings in our find/find all
paragraph_find = soup.find_all("p", string=re.compile("Some"))
print(paragraph_find)

print("")
header_find = soup.find_all("h2", string=re.compile("(H|h)eader"))
print(header_find)

print("")
#Select css selector
content = soup.select("div > p")
print(content)

print("")
bold_text = soup.select("p#paragraph-id b")
print(bold_text)

print("")
paragraphs_find = soup.select("body > p")
print(paragraph_find)

for find in paragraph_find:
    print(find.select("i"))

print("")

#Get different Properties
header_text = soup.find("h2")
print(header_text.string)

div_find = soup.find("div")
print(div_find.get_text())

#Get a specific property from an element
print("")
link = soup.find("a")
print(link['href'])

paragraph_property = soup.select("p#paragraph-id")
print(paragraph_property[0]['id'])

print("")
#Know the terms: Parent Sibling Child
sibling = soup.body.find('div').find_next_sibling()
print(sibling)  