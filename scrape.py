import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import column

HTML_FILE = 'List of PlayStation 2 games (A–K) - Wikipedia.html'
DOT = '•'

with open(HTML_FILE, encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

table = soup.find(id='softwarelist')

allRows = list(table.tbody.find_all('tr'))

data = []

for row in allRows[1:]:
    titleCell, devCell, pubCell, dateCell = row.find_all('td')[:4]

    title = titleCell.text.strip()
    dev = devCell.text.strip()
    pub = pubCell.text.strip()
    date = dateCell.text.strip()

    data.append((title, dev, pub, date))

df = pd.DataFrame(data, columns=['titulo(s)', 'desenvolvedora(s)', 'editora(s)', 'data'])

print(df)

df.to_csv('jogos_play2.csv', index=False)