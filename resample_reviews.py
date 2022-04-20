

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("google/pasha_turkish_grill_restaurant.xlsx")
df['date'] =  pd.to_datetime(df['date'], format='%Y-%d-%m')
df = df.set_index('date')
df = pd.Series(df.iloc[:, 1])



df = pd.Series(df.resample('50D').mean())
df = (df.ffill()+df.bfill())/2
df = df.bfill().ffill()
print(df)

pd.plotting.autocorrelation_plot(df)
plt.show()


'''
import matplotlib.pyplot as plt


plt.plot(list(df.index.values), df.iloc[:])
plt.show()


out = {}

for i in list(x.index):
    if str(df.at[i]) != 'NaN': out[i] = df.at[i]

'''
