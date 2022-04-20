
from google_review_scraper import scrape_reviews
from formatting_google_data import format_excel
import pandas as pd
import time
from tqdm import tqdm

f = open('wronguns.txt', 'w+')

df = pd.read_csv('google_ids_main.csv')

for i in tqdm(range(len(df))):
    try:
        scrape_reviews(df.iat[i, 0], df.iat[i, 3])
        format_excel(df.iat[i, 3])
    except:
        f.write(df.iat[i, 3])

    time.sleep(3)

f.close()
