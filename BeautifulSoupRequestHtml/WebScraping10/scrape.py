import requests
import datetime
import pandas as pd
from requests_html import HTML

def url_to_file(url, year):

    r = requests.get(url)

    if r.status_code == 200:
        html_text = r.text

        with open(f"world-{year}.html", 'w') as f:
            f.write(html_text)
        
        return html_text
    
    
    return ""

def parse_to_extract(url, year='2020'):
    html_text = url_to_file(url,year)
    r_html = HTML(html=html_text)
    table = r_html.find(".imdb-scroll-table")

    print(table)
    table_data = []
    header_names =[]

    if len(table) == 1:
        #print(table[0].text)
        parsed_table = table[0]
        rows = parsed_table.find('tr')
        header_row = rows[0]
        header_column = header_row.find('th')
        header_names = [x.text for x in header_column]
        
        for row in rows[1:10]:
            cols = row.find('td')
            row_data = []
            #row_data_dict = {}
            for i, col in enumerate(cols):
                header_name = header_names[i]

                row_data_dict[header_name] = col.text
                row_data.append(col.text)

            table_data.append(row_data)

    df = pd.DataFrame(table_data, columns=header_names)
    df.to_csv('movies.csv', index=False)

    print(header_names)
    print(table_data)

def run(start_year=None, years_ago = 10):

    assert isinstance(start_year, int)
    assert len(f"{start_year}") == 4
    now = datetime.datetime.now()
    year = now.year
    url = f'https://www.boxofficemojo.com/year/world/{start_year}/'
    parse_to_extract(url, start_year)

if __name__ == '__main__':  
    run(2015)