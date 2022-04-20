

import pandas as pd
import datetime
import time
import numpy as np
import statsmodels.api as sm
from tqdm import tqdm




def conduct_test(name):
    path = name.lower().replace(' ', '_')
    df = pd.read_excel('google/' + path + '.xlsx', index_col=0)


    for i in range(len(df)):
        df.iat[i, 0] = time.mktime(datetime.datetime(int(str(df.iat[i, 0]).split('-')[0]), int(str(df.iat[i, 0]).split('-')[2][:2]), int(str(df.iat[i, 0]).split('-')[1]), 0, 0).timetuple())

    df.to_excel('t.xlsx')

    X = np.array(df.iloc[:, 0].values, dtype=float)
    X = sm.add_constant(X)
    Y = np.array(df.iloc[:, 1].values, dtype=float)


    model = sm.OLS(Y, X)
    results = model.fit()
    return results.params[1]*31536000, results.pvalues[1]*100, -1*results.params[1]*31536000*(100-results.pvalues[1]*100)

df = pd.read_csv('google_ids_main.csv')

f = open('rating_trends.tsv', 'w')

for i in tqdm(range(len(df))):
    try:
        j, k, l = conduct_test(df.iat[i, 3])
        f.write('{}\t{}\t{}\t{}\n'.format(df.iat[i, 3], j, k, l))
    except Exception as e:
        pass


f.close()
