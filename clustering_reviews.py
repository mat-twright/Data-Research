

import pandas as pd
from scipy import stats
import time

start_time = time.time()


#df = pd.read_excel('google/pasha_turkish_grill_restaurant.xlsx')
#df = df.iloc[:, 1:3].set_index('date')
#print(df.shape)

print('LOADING DATA')



df = pd.read_excel("google/ocean_basket_bromley.xlsx")
df['date'] =  pd.to_datetime(df['date'], format='%Y-%d-%m')
df = df.iloc[:, [1,2]]
df['copyDate'] = df['date']
df = df.set_index('copyDate')

for i in range(len(df)):
    df.iat[i, 0] = df.iat[i, 0].timestamp()

df = df.sort_index()


print('CLUSTERING')

from tslearn.clustering import TimeSeriesKMeans
model = TimeSeriesKMeans(n_clusters=2, metric="dtw", max_iter=10)
model.fit(df)
l = model.labels_
out = {}

print('SORTING')

zeroes = []
ones = []


for i, j in enumerate(df.index.values):
    if l[i] == 0:
        zeroes.append(df.iat[i, 1])
    else:
        ones.append(df.iat[i, 1])


out = pd.Series(l, index=df.index)
if out.iat[0] == 1:
    for i in list(out.index):
        out.at[i] = abs(out.at[i]-1)
    z = ones
    ones = zeroes
    zeroes = z
out.to_csv('clustering_reviews.csv')

switch_date = pd.to_datetime('12-12-2025', format='%d-%m-%Y')

for i in list(out.index.values):
    try:
        if out[i] == 1 and i < switch_date:
            switch_date = i
    except:
        if out[i][0] == 1 and i < switch_date:
            switch_date = i


p = stats.ttest_ind(zeroes, ones, equal_var=False ).pvalue
print('p-value: {}'.format(p))
if p < 0.1:
    print(sum(zeroes)/len(zeroes), sum(ones)/len(ones))
    print('The mean rating has gotten significantly', end=' ')
    if sum(zeroes)/len(zeroes) > sum(ones)/len(ones):
        print('lower', end=' ')
    else:
        print('higher', end=' ')
    print('since', end=' ')
    print(switch_date)

else:
    print('No significant change')


print('TIME', time.time()-start_time)
