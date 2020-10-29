import requests
from bs4 import BeautifulSoup

url = 'https://www.skysports.com/premier-league-table'

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

league_table = soup.find("table", {"class": "standing-table__table"})

for team in league_table.find_all('tbody'):
    rows = team.find_all('tr')

    for row in rows:
        pl_team = row.find('a', {"class": "standing-table__cell--name-link"}).text
        points = row.find_all('td', {"class": "standing-table__cell"})[9].text
        print(pl_team)
        print(points)
    


