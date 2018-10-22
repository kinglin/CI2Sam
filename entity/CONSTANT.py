from datetime import date

# file path
RAW_DATA_PATH = '/Users/lince/Desktop/NUS/03_CA/CA_11_CI2/raw_data/interpolate_mod_trading_df_day12pm.csv'
OUTPUT_PATH = '/Users/lince/Desktop/NUS/03_CA/CA_11_CI2/output/div50_r10_p10_g10/'

# group split
TRADE_DATE = date(2014, 1, 2)
DIV_30 = 50 # 30

# MA related
MA_METHODS = ['sma', 'ama', 'tma', 'tpma']# ['sma', 'ama', 'tma', 'tpma']
MA_LONG_WINDOW_SIZES = [10, 20, 50, 100] #[10, 20, 50, 100, 150, 200]
MA_SHORT_WINDOW_SIZES = [3, 5, 10] #[2, 3, 5, 10, 15, 20]

MA_DEFAULT_COL = 'close'
EXTENT_GROUPS = 7
EXTENT = ['EL', 'VL', 'L', 'M', 'H', 'VH', 'EH']


# three status
STATUS_TRAIN = 'train'
STATUS_SELECTION = 'selection'
STATUS_TEST = 'test'

# GA related
NUM_OF_RULES_PER_INDV = 10
NUM_OF_POPULATION = 10
NUM_OF_GENERATION = 10
PROB_CROSSOVER = 0.7
PROB_MUTATE = 1
PROB_MUTATE_CROSSOVER = 0.5
PROB_MUTATE_MUTATE = 0.5
POPULATION_BEST_PORTION = 0.2
POPULATION_REMAIN_PORTION = 0.6

# Capital related
ORI_CAP_VALUE = 10000000
VALUE_PER_PRICE = 25
TRANS_THRESHOLD = 30
RF_RATE = 0.04/365
HANDLING_FEE = 0.002
BORROW_INTEREST_FEE = 0.0001
TRANS_HOLD = 'hold'
TRANS_BUY = 'buy'
TRANS_SELL = 'sell'
DEPOSIT = 1.0