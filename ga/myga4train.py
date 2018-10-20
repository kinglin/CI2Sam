from ga.myga import myga
from entity.MF import MF
from capflow.CapFlow import CapFlow
from capflow.DymcShortList import DymcShortList
from capflow.Trans import Trans
from capflow.DymcShortList import ReturnBorrowLog
from entity import CONSTANT
from tqdm import tqdm


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

        def get_rreturn(rlevel, datetime, row, cf, trans, dsl, rbl):
            cur_holding = int(CONSTANT.ORI_CAP_VALUE * rlevel / (row[CONSTANT.MA_DEFAULT_COL] * CONSTANT.DEPOSIT))
            pre_holding = 0 if cf.df.shape[0] == 0 else cf.df['holding'][cf.df.shape[0] - 1]
            if abs(cur_holding - pre_holding) >= CONSTANT.TRANS_THRESHOLD:
                tran = trans.insert(datetime=datetime, cur_holding=cur_holding, high=row['high'], low=row['low'])
                if tran['volume_s'][0] < 0:
                    dsl.insert(datetime=datetime, cost_borrow=tran['cost_borrow'][0], short_left=-tran['volume_s'][0], short_price=row['low'])
                elif tran['volume_s'][0] > 0:
                    ds_up_dict = dsl.update(tran)
                    rbl.insert(datetime=datetime, up_dict=ds_up_dict)
                rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl, tran=tran)
            else:
                rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl)

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

            cf = CapFlow(CapFlow.get_ori_df(data[1].index.values[0]))
            trans = Trans(Trans.get_empty_df())
            dsl = DymcShortList(DymcShortList.get_empty_df())
            rbl = ReturnBorrowLog(ReturnBorrowLog.get_empty_df())

            for datetime, row in tqdm(data[1].iterrows()):
                rlevel = 0
                act = 0
                for rule in individual:
                    diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                    mfvalue = rule.mf(rule.fuzzy_extent, [row[diff_col_name]])
                    if mfvalue[0] > 0:
                        act += 1
                        rlevel += mfvalue[0] * rule.rating_value
                if act > 0:
                    rlevel /= act
                rreturn_t = get_rreturn(rlevel, datetime, row, cf, trans, dsl, rbl)
                rreturn += rreturn_t

            rreturn /= data[1].shape[0]
            print(rreturn)
            return rreturn

        self.fitness_function = fitness
