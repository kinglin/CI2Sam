from entity import CONSTANT
import pandas as pd


class CapFlow:

    def __init__(self, ori_df):
        self.df = ori_df

    @staticmethod
    def get_ori_df(first_index, holding=0, holding_value=0, total_cost_once=0, total_cost_borrow=0, riskfee=0,
                        cash=CONSTANT.ORI_CAP_VALUE, capital_value=CONSTANT.ORI_CAP_VALUE, rreturn=0):
        data = {'datetime': first_index,
                'action': CONSTANT.TRANS_HOLD,
                'holding': holding,
                'holding_value': holding_value,
                'total_cost_once': total_cost_once,
                'total_cost_borrow': total_cost_borrow,
                'riskfee': riskfee,
                'realized_profit': 0,
                'cash': cash,
                'capital_value': capital_value,
                'rreturn': rreturn}
        ori_df = pd.DataFrame.from_dict(data)
        ori_df.set_index('datetime')
        return ori_df

    def insert(self, tran=None, value=None):

        if tran is None:
            pass
        else:
            pass

        return dict()
