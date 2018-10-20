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

tup = (1,2,3)
len(tup)

import random
random.randrange(4)

from entity.Rule import Rule
import copy

def change_value(v1, v2):
    return v2, v1
r1 = Rule(1,2,3,4)
r2 = Rule(5,6,7,8)

r1.l_s_values, r2.l_s_values = r2.l_s_values, r1.l_s_values
r1.fuzzy_extent, r2.fuzzy_extent = r2.fuzzy_extent, r1.fuzzy_extent




cross_rules = [r1, r2]
child_1, child_2 = cross_rules[0], cross_rules[1]

index = random.randrange(1, 4)
if index == 1:
    child_1.l_s_values, child_2.l_s_values = child_2.l_s_values, child_1.l_s_values
    child_1.fuzzy_extent, child_2.fuzzy_extent = child_2.fuzzy_extent, child_1.fuzzy_extent
    child_1.rating_value, child_2.rating_value = child_2.rating_value, child_1.rating_value
elif index == 2:
    child_1.fuzzy_extent, child_2.fuzzy_extent = child_2.fuzzy_extent, child_1.fuzzy_extent
    child_1.rating_value, child_2.rating_value = child_2.rating_value, child_1.rating_value
elif index == 3:
    child_1.rating_value, child_2.rating_value = child_2.rating_value, child_1.rating_value

cross_rules += [child_1, child_2]

import pandas as pd
from entity import CONSTANT
df = pd.DataFrame({'datetime':['t1', 't2', 't3'], 'v1':[1,2,3], 'v2':[7,8,9]})
writer = pd.ExcelWriter(CONSTANT.OUTPUT_PATH + 'test.xlsx')
df.to_excel(writer, 'all_best_individuals')
df.to_excel(writer, 'all_best_individuals1')
writer.save()