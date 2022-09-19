import pandas as pd
import urllib.parse

url_1 = 'https://en.wikipedia.org/wiki/List_of_PlayStation_2_games_(A%E2%80%93K)'
url_2 = 'https://en.wikipedia.org/wiki/List_of_PlayStation_2_games_(L%E2%80%93Z)'

def process_url_dataset(url):

  # Read html_table
  df = pd.read_html(url,attrs = {'id': 'softwarelist'})
  df = df[0]

  # Drop & rename
  df = df.drop("Publisher", axis=1)
  df = df.rename(columns={df.columns[4]: 'EU'})

  # Handling Special Characters
  df[['JP','EU','NA']] = df[['JP','EU','NA']].notnull().astype('int')
  df = df.fillna(0)

  #First English Tittle
  title = df['Title'].str.split("•", n = 1, expand = True)
  df['Title'] =  title[0]
  
  # Creating Region column
  region = df['First released'].str.slice(start=10)
  region = region.str.split(",", n = 1, expand = True)
  df['First Region'] =  region[0]
  df['First released'] = df['First released'].str.slice(stop=10)

  # Find searched text based on start and finish string
  x = urllib.parse.unquote(url)
  file_name = 'jogos_play2'
  file_name = file_name + '_' + x[ x.find('(') + len('('):x.rfind(')')]

  # Generating CSV
  df.to_csv(file_name + '.csv', index=False)

  return df

process_url_dataset(url_1)
process_url_dataset(url_2)