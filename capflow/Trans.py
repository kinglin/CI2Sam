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

    def insert(self, datetime, cur_holding, high, low):
        pre_holding = 0 if self.df.shape[0] == 0 else self.df['cur'][self.df.shape[0] - 1]
        trans_type = CONSTANT.TRANS_BUY if cur_holding > pre_holding else CONSTANT.TRANS_SELL
        volume_l = max(cur_holding,0) - max(pre_holding,0)
        volume_s = min(cur_holding,0) - min(pre_holding,0)
        cost_once = abs(cur_holding - pre_holding) * CONSTANT.HANDLING_FEE * (high if trans_type == CONSTANT.TRANS_BUY else low)
        cost_borrow = abs(min(volume_s,0)) * low * CONSTANT.BORROW_INTEREST_FEE
        realized_profit = -low * (cur_holding - pre_holding)

        tran = {'datetime': [datetime],
                'pre': [pre_holding],
                'cur': [cur_holding],
                'type': [trans_type],
                'volume_l': [volume_l],
                'volume_s': [volume_s],
                'cost_once': [cost_once],
                'cost_borrow': [cost_borrow],
                'short_price': [0] if volume_s == 0 else [low],
                'realized_profit': [realized_profit]}
        tran_df = pd.DataFrame.from_dict(tran)
        self.df = self.df.append(tran_df, ignore_index=True)
        return tran
