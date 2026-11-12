import requests
import pandas as pd
import io

# URL to scrape
url = "https://www.ncaa.com/stats/basketball-women/d1/current/team/114"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers)

# Pandas can read HTML tables directly from a webpage
tables = pd.read_html(io.StringIO(response.text), flavor='lxml')

# Grab the first table and save it to a CSV file
df = tables [0]
df.to_csv("ncee_fg_stats.csv", index=False)
print("Data scraped and saved to ncee_fg_stats.csv")