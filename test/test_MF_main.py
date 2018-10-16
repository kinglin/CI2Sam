import pandas as pd
from entity import CONSTANT
from entity.MF import MF

interpolate_mod_trading_df = pd.read_csv(CONSTANT.RAW_DATA_PATH, index_col=0)
interpolate_mod_trading_df.index = pd.to_datetime(interpolate_mod_trading_df.index)

interpolate_mod_trading_df['SMA_60'] = interpolate_mod_trading_df['High'].rolling(window=60).mean()
interpolate_mod_trading_df['SMA_15'] = interpolate_mod_trading_df['High'].rolling(window=15).mean()
interpolate_mod_trading_df['MA_diff'] = interpolate_mod_trading_df['SMA_15'] - interpolate_mod_trading_df['SMA_60']

sorted_diff = interpolate_mod_trading_df['MA_diff'].sort_values(ascending=True).dropna()
sorted_diff.reset_index(inplace=True, drop=True)

mf_instance = MF(sorted_diff)
mf_function = mf_instance.get_mf()

extent = 0
diff = -20
value = mf_function(extent, diff)
value1 = mf_function(6, diff)
pass