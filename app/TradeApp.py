import pandas as pd
from app.DataHelper import DataHelper
from app.TradeHelper import TradeHelper
from entity.MA import MA
from entity import CONSTANT
import warnings


def main():

    group_div = DataHelper.DIV_30

    raw_data = pd.read_csv(CONSTANT.RAW_DATA_PATH, index_col=0)
    raw_data.index = pd.to_datetime(raw_data.index)
    raw_data = price_to_value(raw_data)
    raw_data_ma_diffs = MA(raw_data).get_df_with_ma_diffs()

    dh = DataHelper(raw_data_ma_diffs, group_div)
    train_groups, selection_groups, test_groups, trade_index = dh.get_data_groups()

    th_pure_train = TradeHelper(raw_data_ma_diffs, train_groups[0:trade_index],
                                selection_groups[0:trade_index],
                                test_groups[0:trade_index])
    best_individuals_from_pure_training = th_pure_train.get_best_individuals()

    th_trade = TradeHelper(raw_data_ma_diffs, train_groups[trade_index:len(train_groups)],
                           selection_groups[trade_index:len(selection_groups)],
                           test_groups[trade_index:len(test_groups)])
    total_profit = th_trade.get_total_test_profit(best_individuals_from_pure_training)

    print(total_profit)


def price_to_value(raw_data):

    cols = raw_data.columns.values
    for col in cols:
        if col is not 'datetime':
            raw_data[col] = raw_data[col] * CONSTANT.VALUE_PER_PRICE
    return raw_data

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    main()
