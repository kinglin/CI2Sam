from ga.myga import myga
from entity.MF import MF
from pyeasyga import pyeasyga
import random
from operator import attrgetter
from entity.MA import MA
from entity import CONSTANT
from entity.Rule import Rule


class myga4train(myga):

    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):

        myga.__init__(self,
                      seed_data=seed_data,
                      population_size=population_size,
                      generations=generations,
                      crossover_probability=crossover_probability,
                      mutation_probability=mutation_probability,
                      elitism=elitism,
                      maximise_fitness=maximise_fitness)

        def fitness(individual, data):
            rreturn = 0
            for rule in individual:
                diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                pre_diff = data[0][diff_col_name]
                cur_diff = data[1][diff_col_name]
                total_diff = pre_diff.append(cur_diff, ignore_index=True)
                mf = MF(total_diff).get_mf()
                rule.mf = mf

            for _, row in data[1].iterrows():
                rlevel = 0
                act = 0
                for rule in individual:
                    diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                    mfvalue = rule.mf(rule.fuzzy_extent, [row[diff_col_name]])
                    if mfvalue > 0:
                        act += 1
                        rlevel += mfvalue * rule.rating_value
                if act > 0:
                    rlevel /= act
                rreturn_t = get_rreturn(rlevel, row)

            return rreturn

        self.fitness_function = fitness


import pandas as pd
d = {'col1': [1, 2], 'col2': [2, 4]}
df = pd.DataFrame(data=d)
for _, row in df.iterrows():
    rvalue = row['col2']
    print(rvalue)