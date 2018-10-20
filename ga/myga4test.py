from entity import CONSTANT
from tqdm import tqdm


class myga4test():

    def __init__(self, data, individual, cf, trans, dsl, rbl):
        self.data = data
        self.individual = individual
        self.cf = cf
        self.trans = trans
        self.dsl = dsl
        self.rbl = rbl

    def get_rreturn(self, rlevel, datetime, row, cf, trans, dsl, rbl):
        cur_holding = int(CONSTANT.ORI_CAP_VALUE * rlevel / (row[CONSTANT.MA_DEFAULT_COL] * CONSTANT.DEPOSIT))
        pre_holding = 0 if cf.df.shape[0] == 0 else cf.df['holding'][cf.df.shape[0] - 1]
        if abs(cur_holding - pre_holding) >= CONSTANT.TRANS_THRESHOLD:
            tran = trans.insert(datetime=datetime, cur_holding=cur_holding, high=row['high'], low=row['low'])
            if tran['volume_s'][0] < 0:
                dsl.insert(datetime=datetime, cost_borrow=tran['cost_borrow'][0], short_left=-tran['volume_s'][0],
                           short_price=row['low'])
            elif tran['volume_s'][0] > 0:
                ds_up_dict = dsl.update(tran)
                rbl.insert(datetime=datetime, up_dict=ds_up_dict)
            rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl, tran=tran)
        else:
            rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl)

        return rreturn

    def fitness(self):
        rreturn = 0

        for datetime, row in tqdm(self.data.iterrows()):
            rlevel = 0
            act = 0
            for rule in self.individual:
                diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                mfvalue = rule.mf(rule.fuzzy_extent, [row[diff_col_name]])
                if mfvalue[0] > 0:
                    act += 1
                    rlevel += mfvalue[0] * rule.rating_value
            if act > 0:
                rlevel /= act
            rreturn_t = self.get_rreturn(rlevel, datetime, row, self.cf, self.trans, self.dsl, self.rbl)
            rreturn += rreturn_t

        rreturn /= self.data[1].shape[0]
        print(rreturn)
        return rreturn