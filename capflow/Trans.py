from entity import CONSTANT
import pandas as pd


class Trans:
    def __init__(self, ori_df):
        self.df = ori_df

    @staticmethod
    def get_empty_df():
        ori_df = pd.DataFrame(columns=['datetime', 'pre', 'cur', 'type', 'volume_l',
                                       'volume_s', 'cost_once', 'cost_borrow',
                                       'short_price', 'realized_profit'])
        return ori_df

    def insert(self, datatime, cur_holding, high, low):
        pre_holding = 0 if self.df.shape[0] == 0 else self.df['cur'][self.df.shape[0] - 1]
        type = CONSTANT.TRANS_BUY if cur_holding > pre_holding else CONSTANT.TRANS_SELL
        volume_l = cur_holding - max(0, pre_holding) if cur_holding >= 0 else (-pre_holding if pre_holding > 0 else 0)
        volume_s = cur_holding - min(0, pre_holding)
        cost_once = abs(cur_holding - pre_holding) * CONSTANT.HANDLING_FEE * (high if type == CONSTANT.TRANS_BUY else low)
        cost_borrow = abs(volume_s) * low * CONSTANT.BORROW_INTEREST_FEE
        realized_profit = -low * (cur_holding - pre_holding)

        trans = {'datetime': datatime,
                'pre': pre_holding,
                'cur': cur_holding,
                'type': type,
                'volume_l': volume_l,
                'volume_s': volume_s,
                'cost_once': cost_once,
                'cost_borrow': cost_borrow,
                'short_price': low,
                'realized_profit': realized_profit}
        trans_df = pd.DataFrame.from_dict(trans)
        self.df.append(trans_df, ignore_index=True)
        return trans


# import pandas as pd
#
# data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
# test_df = pd.DataFrame.from_dict(data)
# test_df['col_1'][test_df.shape[0] - 1]
# max(2, 4)
