import pandas as pd
# from datetime import date
from MA import MA

interpolate_mod_trading_df = pd.read_csv("interpolate_mod_trading.csv", index_col=0)
interpolate_mod_trading_df.index = pd.to_datetime(interpolate_mod_trading_df.index)

ma_instance = MA(interpolate_mod_trading_df)
# print(MA.get_m_n_combs())

result_df = ma_instance.get_df_with_ma_diffs()

pass