from ga.myga import myga
from entity.MF import MF
from capflow.CapFlow import CapFlow
from capflow.DymcShortList import DymcShortList
from capflow.Trans import Trans
from capflow.DymcShortList import ReturnBorrowLog
from pyeasyga import pyeasyga
import random
from operator import attrgetter
from entity.MA import MA
from entity import CONSTANT
from entity.Rule import Rule


class myga4train(myga):

    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):

        myga.__init__(self,
                      seed_data=seed_data,
                      population_size=population_size,
                      generations=generations,
                      crossover_probability=crossover_probability,
                      mutation_probability=mutation_probability,
                      elitism=elitism,
                      maximise_fitness=maximise_fitness)

        def get_rreturn(rlevel, row, cf, trans, dsl, rbl):
            cur_holding = CONSTANT.ORI_CAP_VALUE * rlevel / (row[CONSTANT.MA_DEFAULT_COL] * CONSTANT.DEPOSIT)
            pre_holding = 0 if cf.df.shape[0] == 0 else cf.df['cur'][cf.df.shape[0] - 1]
            if abs(cur_holding - pre_holding) >= CONSTANT.TRANS_THRESHOLD:
                tran = trans.insert(datetime=row['datetime'], cur_holding=cur_holding, high=row['high'], low=row['low'])
                if tran['volume_s'] < 0:
                    dsl.insert(datetime=row['datetime'], cost_borrow=tran['cost_borrow'], short_left=-tran['volume_s'], short_price=row['low'])
                elif tran['volume_s'] > 0:
                    ds_up_dict = dsl.update(tran)
                    rbl.insert(datetime=row['datetime'], up_dict=ds_up_dict)
                rreturn = cf.insert(tran=tran, value=row['low'])
            else:
                rreturn = cf.insert(value=row['low'])

            return rreturn

        def fitness(individual, data):
            rreturn = 0
            for rule in individual:
                diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                pre_diff = data[0][diff_col_name]
                cur_diff = data[1][diff_col_name]
                total_diff = pre_diff.append(cur_diff, ignore_index=True)
                mf = MF(total_diff).get_mf()
                rule.mf = mf

            cf = CapFlow(CapFlow.get_ori_df(data[1]['datetime'][0]))
            trans = Trans(Trans.get_empty_df())
            dsl = DymcShortList(DymcShortList.get_empty_df())
            rbl = ReturnBorrowLog(ReturnBorrowLog.get_empty_df())

            for _, row in data[1].iterrows():
                rlevel = 0
                act = 0
                for rule in individual:
                    diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                    mfvalue = rule.mf(rule.fuzzy_extent, [row[diff_col_name]])
                    if mfvalue > 0:
                        act += 1
                        rlevel += mfvalue * rule.rating_value
                if act > 0:
                    rlevel /= act
                rreturn_t = get_rreturn(rlevel, row, cf, trans, dsl, rbl)
                rreturn += rreturn_t

            rreturn /= data[1].shape[0]

            return rreturn

        self.fitness_function = fitness





import pandas as pd

d = {'t1': [2, 6, 6, 4], 't2': [1, 2, 3, 3], 'size': [3, 4, 5, 4], 'm': [2, 6, 6, 4]}
df = pd.DataFrame(data=d)
df
row = df.loc[df['m'] == df['m'].max()][0:1]
row

df.loc[(df['m'] == df['m'].max()) & (df['t1'] == row['t1'].values[0]) & (df['t2'] == row['t2'].values[0]), 'size'] = row['size'].values[0] - 4
df

df = df[df['size']>0]
df

for _, row in df.iterrows():
    rvalue = row['col2']
    print(rvalue)
