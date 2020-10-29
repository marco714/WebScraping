from requests_html import HTML

with open("snippet.html") as html_file:

    source = html_file.read()
    html = HTML(html=source)
    html.render()
    
match = html.find('#footer', first=True)
print(match.text)
#print(html.text)

articles = html.find('div.article')

for article in articles:

    headline = article.find('h2', first=True).text.strip()
    summary = article.find('p', first=True).text.strip()

print(summary)
print(headline)
print(articles)