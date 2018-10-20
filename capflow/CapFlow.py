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

    def insert(self, row, dsl, tran=None):

        action = CONSTANT.TRANS_HOLD if tran is None else tran['type']
        holding = self.get_last_value('holding') if tran is None else tran['cur']
        holding_value = holding * row['low']
        total_cost_once = self.get_last_value('total_cost_once') + (0 if tran is None else tran['cost_once'])
        total_cost_borrow = self.get_last_value('total_cost_borrow') + dsl['cost_borrow'].sum()
        riskfee = self.get_last_value('riskfee') + self.get_last_value('cash') * CONSTANT.RF_RATE
        realized_profit = self.get_last_value('realized_profit') + (0 if tran is None else tran['realized_profit'])
        cash = CONSTANT.ORI_CAP_VALUE + riskfee + realized_profit - total_cost_borrow - total_cost_once
        capital_value = holding_value + cash
        rreturn = (capital_value - CONSTANT.ORI_CAP_VALUE) / CONSTANT.ORI_CAP_VALUE

        data = {'datetime': row['datetime'],
                'action': action,
                'holding': holding,
                'holding_value': holding_value,
                'total_cost_once': total_cost_once,
                'total_cost_borrow': total_cost_borrow,
                'riskfee': riskfee,
                'realized_profit': realized_profit,
                'cash': cash,
                'capital_value': capital_value,
                'rreturn': rreturn}
        data_df = pd.DataFrame.from_dict(tran)
        self.df.append(data_df, ignore_index=True)

        return data

    def get_last_value(self, col_name, default_value=0):
        return default_value if self.df.shape[0] == 0 else self.df[col_name][self.df.shape[0] - 1]
