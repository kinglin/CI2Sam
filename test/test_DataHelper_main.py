import pandas as pd
# from datetime import date
from entity import CONSTANT
from app.DataHelper import DataHelper

interpolate_mod_trading_df = pd.read_csv(CONSTANT.RAW_DATA_PATH, index_col=0)
interpolate_mod_trading_df.index = pd.to_datetime(interpolate_mod_trading_df.index)

data_helper = DataHelper(interpolate_mod_trading_df, 30)
data_helper.get_unique_dates()

train_groups, selection_groups, test_groups, trade_in_test_index = data_helper.get_data_groups()

pass