
import pandas as pd
import preprocessor as p
import re
import string
from nltk.corpus import stopwords

regex = re.compile('[%s]' % re.escape(string.punctuation))

stop_words = set(stopwords.words("english"))

def remove_stopwords(m):
    m = " ".join([word for word in m.split() if word not in stop_words])
    return m.replace("i'm", '')

df = pd.read_csv('RUN_store_tweets.csv')

def clean(t):
    t = t[1:].lower()
    t = " ".join(t.split("\\n"))
    t = t.replace("'", '')
    t = re.sub("@\S+", "", t)
    t = p.clean(t)
    t = t.replace('\n', ' ')
    t = regex.sub(' ', t)
    t = t.replace(' xe2 x80 x99', "'").replace(' xc3 xa9', 'e')
    t = t.replace('xe2', '').replace('x80', '').replace('x9c', '').replace('x99', '').replace('x98', '').replace('xa6', '').replace('x9d', '').replace('x93', '').replace('x81', '').replace('xf0', '').replace('x9f', '').replace('x89', '').replace('x8c', '').replace('xb4', '').replace('x8a', '').replace('xb1', '').replace('xc2', '')
    t = " ".join([x for x in t.split(' ') if x != ''])
    if t[:2] == 'rt': t = t[3:]
    t = t.replace(' amp ', ' and ')
    return t


for i in range(len(df)):

    df.iat[i, 2] = clean(df.iat[i, 2])

    df.iat[i, 2] = remove_stopwords(df.iat[i, 2])

print(df)



df.to_csv('RUN_cleaned_no_stopwords.tsv', sep='\t')
