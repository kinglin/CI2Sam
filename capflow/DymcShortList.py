import pandas as pd
from entity import CONSTANT


class DymcShortList:

    def __init__(self, ori_df):
        self.df = ori_df

    @staticmethod
    def get_empty_df():
        ori_df = pd.DataFrame(columns=['datetime', 'cost_borrow', 'short_left', 'short_price'])
        return ori_df

    def insert(self, datetime, cost_borrow, short_left, short_price):

        data = {'datetime': [datetime],
                 'cost_borrow': [cost_borrow],
                 'short_left': [short_left],
                 'short_price': [short_price]}
        data_df = pd.DataFrame(data)
        self.df = self.df.append(data_df, ignore_index=True)

    def update(self, tran):

        updict = dict()

        volume_s = tran['volume_s'][0]

        while True:
            short_row = self.df.loc[self.df['short_price'] == self.df['short_price'].max(), :][0:1]
            if volume_s <= short_row['short_left'].values[0]:
                self.df.loc[(self.df['short_price'] == self.df['short_price'].max())
                            & (self.df['datetime'] == short_row['datetime'].values[0]), 'short_left'] = \
                    short_row['short_left'].values[0] - volume_s
                self.df.loc[(self.df['short_price'] == self.df['short_price'].max())
                            & (self.df['datetime'] == short_row['datetime'].values[0]), 'cost_borrow'] = \
                    (short_row['short_left'].values[0] - volume_s) * short_row['short_price'].values[0] * CONSTANT.BORROW_INTEREST_FEE
                updict[short_row['datetime'].values[0]] = volume_s
                break
            else:
                self.df.loc[(self.df['short_price'] == self.df['short_price'].max())
                            & (self.df['datetime'] == short_row['datetime'].values[0]), 'short_left'] = 0
                updict[short_row['datetime'].values[0]] = short_row['short_left'].values[0]
                volume_s = volume_s - short_row['short_left'].values[0]
            self.df = self.df[self.df['short_left'] > 0]

        return updict


class ReturnBorrowLog:

    def __init__(self, ori_df):
        self.df = ori_df

    @staticmethod
    def get_empty_df():
        ori_df = pd.DataFrame(columns=['from_datetime', 'target_datetime', 'volume'])
        return ori_df

    def insert(self, datetime, up_dict):
        for key in up_dict.keys():
            data = {'from_datetime': [datetime],
                    'target_datetime': [key],
                    'volume': [up_dict[key]]}
            self.df = self.df.append(pd.DataFrame.from_dict(data.copy()), ignore_index=True)