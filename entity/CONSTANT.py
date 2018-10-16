# file path
RAW_DATA_PATH = '/Users/lince/Desktop/NUS/03_CA/CA_11_CI2/raw_data/interpolate_mod_trading.csv'

# MA related
# M stands for long period, n stands for short period
MA_M_VALUES = [10, 20, 50, 100, 150, 200]
MA_N_VALUES = [1, 3, 5, 10, 15, 20]

MA_METHODS = ['sma', 'ama', 'tma', 'tpma']
MA_DEFAULT_COL = 'close'
EXTENT_GROUPS = 7

# three status
STATUS_TRAIN = 'train'
STATUS_SELECTION = 'selection'
STATUS_TEST = 'test'

# GA related
NUM_OF_RULES_PER_INDV = 10
NUM_OF_POPULATION = 20
NUM_OF_GENERATION = 10
PROB_CROSSOVER = 0.7
PROB_MUTATE = 0.1