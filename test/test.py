import pandas as pd

d = {'t1': [2, 6, 6, 4], 't2': [1, 2, 3, 3], 'size': [3, 4, 5, 4], 'm': [2, 6, 6, 4]}
df = pd.DataFrame(data=d)
df
df['t1'][0]

cols = df.columns.values
for col in cols:
    if col is not 't1':
        df[col] = df[col] * 2
df

row = df.loc[df['m'] == df['m'].max()][0:1]
row

df.loc[(df['m'] == df['m'].max()) & (df['t1'] == row['t1'].values[0]) & (df['t2'] == row['t2'].values[0]), 'size'] = row['size'].values[0] - 4
df

df = df[df['size']>0]
df

total = df['size'].apply(lambda x: x.sum(), axis=0)
total

number = df['size'].sum()
number

for _, row in df.iterrows():
    rvalue = row['col2']
    print(rvalue)

mylist = [1,2,3,4,5]
mylist.append(6)
mylist

for i in range(2):
    print(i)



import pandas as pd
data = {'datetime': 'a',
        'action': 1}
ori_df = pd.DataFrame(data, index='datetime')

int(-5.234)

import pandas as pd
ori_df = pd.DataFrame(columns=['datetime', 'pre', 'cur'])
ori_df
tran = {'datetime': ['1'],'pre': [2],'cur': [3]}
tran_df = pd.DataFrame.from_dict(tran)
tran_df
ori_df = ori_df.append(tran_df, ignore_index=True)
ori_df


import pandas as pd
df = pd.DataFrame({'datetime':['t1', 't2', 't3'], 'v1':[1,2,3], 'v2':[7,8,9]})
row = df.loc[df['v1'] == df['v1'].max(), :][0:1]
row['datetime'].values[0]


df.set_index(['datetime'], inplace=True)

for index, row in df.iterrows():
    print(row.name)

type(row.name)