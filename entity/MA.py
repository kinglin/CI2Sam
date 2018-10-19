import pandas as pd
import numpy as np
from entity import CONSTANT
import talib


class MA:

    def __init__(self, df):
        self.df = df

    @staticmethod
    def get_l_s_win_combs():
        combs = []
        for m in CONSTANT.MA_LONG_WINDOW_SIZES:
            for n in CONSTANT.MA_SHORT_WINDOW_SIZES:
                if m > n:
                    combs.append((m, n))
        return combs

    def get_df_with_ma_diffs(self, methods=CONSTANT.MA_METHODS, default_col=CONSTANT.MA_DEFAULT_COL):
        result_df = self.df.copy()
        drop_col = []
        combs = MA.get_l_s_win_combs()
        for col in self.df.columns:
            drop_col.append(col)
        for comb in combs:
            title = "_{}_{}".format(comb[1], comb[0])  # _n_m
            sma_diff, ama_diff, tpma_diff, tma_diff = self.get_ma_set_diff(result_df, comb, default_col)

            temp_df = self.df.copy()
            if 'sma' in methods:
                temp_df['sma'+title] = sma_diff
            if 'ama' in methods:
                temp_df['ama' + title] = ama_diff
            if 'tpma' in methods:
                temp_df['tpma' + title] = tpma_diff
            if 'tma' in methods:
                temp_df['tma' + title] = tma_diff
            temp_df.drop(columns=drop_col, inplace=True)

            result_df = pd.concat([result_df, temp_df], axis=1)
        return result_df

    def get_ma_set_diff(self, df, period, default_col):
        print(period)
        open_price = np.array(df['Open'], dtype=float)
        high_price = np.array(df['High'], dtype=float)
        low_price = np.array(df['Low'], dtype=float)
        close_price = np.array(df['Close'], dtype=float)
        # volume = np.array(df['Volume'], dtype=float)

        target = close_price
        if default_col== "open":
            target = open_price
        elif default_col== "high":
            target = high_price
        elif default_col== "low":
            target = low_price

        # m
        # Simple Moving Average (SMA)
        sma_m = talib.SMA(target, timeperiod=period[0])
        # Adaptive Moving Average (AMA)
        ama_m = talib.KAMA(target, timeperiod=period[0])
        # Typical Price Moving Average (TPMA)
        typical_price_m = talib.TYPPRICE(high_price, low_price, close_price)
        tpma_m = talib.SMA(typical_price_m, timeperiod=period[0])
        # Triangular Moving Average (TMA)
        tma_m = talib.TRIMA(target, timeperiod=period[0])

        # n
        # Simple Moving Average (SMA)
        sma_n = talib.SMA(target, timeperiod=period[1])
        # Adaptive Moving Average (AMA)
        ama_n = talib.KAMA(target, timeperiod=period[1])
        # Typical Price Moving Average (TPMA)
        typical_price_n = talib.TYPPRICE(high_price, low_price, close_price)
        tpma_n = talib.SMA(typical_price_n, timeperiod=period[1])
        # Triangular Moving Average (TMA)
        tma_n = talib.TRIMA(target, timeperiod=period[1])

        sma_diff = sma_n - sma_m
        ama_diff = ama_n - ama_m
        tpma_diff = tpma_n - tpma_m
        tma_diff = tma_n - tma_m

        return sma_diff, ama_diff, tpma_diff, tma_diff
