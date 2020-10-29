from requests_html import HTML, HTMLSession
import csv

csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'Summary', 'Video'])


session = HTMLSession()
r = session.get('https://coreyms.com/')

print(r.html.text)
for link in r.html.links:

    print(link)

articles = r.html.find('article')

for article in articles:
    headline = article.find('.entry-title-link', first=True).text
    print(headline)

    summary = article.find('.entry-content', first=True).text
    print(summary)

    try:
        vid_source = article.find('iframe', first=True).attrs['src']
        vid_id = vid_source.split("/")[4]
        vid_id = vid_id.split("?")[0]

    
    except NameError as e:
        yt_link = None
    except AttributeError as e:
        yt_link = None

    print("")
    yt_link = f"https://youtube.com/watch?v={vid_id}"
    print(yt_link)

    csv_writer.writerow(([headline, summary,yt_link]))

csv_file.close()