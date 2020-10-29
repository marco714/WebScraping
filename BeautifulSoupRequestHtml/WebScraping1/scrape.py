from bs4 import BeautifulSoup
import requests

with open('index.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')



for article in soup.find_all('div', class_='article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)
    

#article = soup.find('div', class_='article')
#print(article)

#headline = article.h2.a.text
#print(headline)

#summary = article.p.text
#print(summary)





#match1 = soup.title.text
#match2 = soup.find('div', class_='footer')
#print(match2)
#print(match1)*/
#print(soup.prettify())