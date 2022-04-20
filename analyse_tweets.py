
import pandas as pd
from tqdm import tqdm

df = pd.read_csv('RUN_cleaned_no_stopwords.tsv', delimiter='\t', index_col=0).fillna('')


import gensim
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

print('LOADING WORD2VEC MODEL')
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print('MODEL LOADED')

keyword = 'ukraine'

out = {}

for i in tqdm(range(len(df))):
    count = 0
    l = 0
    j = df.iat[i, 2].split(' ')
    for k in j:
        try:
            l += model.similarity(keyword, k)
            count += 1
        except:
            pass
    try:
        out[df.iat[i, 1]] = l/count
    except:
        pass



df = pd.Series(out)

df.index = pd.to_datetime(df.index)# format='%Y-%d-%m %H:%M:$S+00:00')
df = pd.Series(df.resample('50D').mean())
df = (df.ffill()+df.bfill())/2
df = df.bfill().ffill()
df.index = pd.to_datetime(df.index).strftime('%d-%m-%Y')

df.to_excel('run_keyword_tracker.xlsx')






'''

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


corpus = ''

for i in range(len(df)):
    corpus += df.iat[i, 3]

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(corpus)

# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()
'''
