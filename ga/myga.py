from pyeasyga import pyeasyga
from entity.MA import MA
import random
from entity.Rule import Rule
import copy
from entity.MF import MF
from capflow.CapFlow import CapFlow
from capflow.DymcShortList import DymcShortList
from capflow.Trans import Trans
from capflow.DymcShortList import ReturnBorrowLog
from entity import CONSTANT
# from tqdm import tqdm


class myga(pyeasyga.GeneticAlgorithm):

    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):

        pyeasyga.GeneticAlgorithm.__init__(self, seed_data,
                                           population_size=population_size,
                                           generations=generations,
                                           crossover_probability=crossover_probability,
                                           mutation_probability=mutation_probability,
                                           elitism=elitism,
                                           maximise_fitness=maximise_fitness)

        self.ma_combs = MA.get_l_s_win_combs()

        def my_create_individual(seed_data):
            rules = []
            for _ in range(CONSTANT.NUM_OF_RULES_PER_INDV):
                rule = Rule(random.choice(CONSTANT.MA_METHODS),
                            random.choice(self.ma_combs),
                            random.choice(CONSTANT.EXTENT),
                            random.randint(-10, 10) / 10)
                rules.append(rule)

            return rules

        def sub_crossover(rule_1, rule_2):
            index = random.randrange(1, 4)
            if index == 1:
                rule_1.l_s_values, rule_2.l_s_values = rule_2.l_s_values, rule_1.l_s_values
                rule_1.fuzzy_extent, rule_2.fuzzy_extent = rule_2.fuzzy_extent, rule_1.fuzzy_extent
                rule_1.rating_value, rule_2.rating_value = rule_2.rating_value, rule_1.rating_value
            elif index == 2:
                rule_1.fuzzy_extent, rule_2.fuzzy_extent = rule_2.fuzzy_extent, rule_1.fuzzy_extent
                rule_1.rating_value, rule_2.rating_value = rule_2.rating_value, rule_1.rating_value
            elif index == 3:
                rule_1.rating_value, rule_2.rating_value = rule_2.rating_value, rule_1.rating_value

        def crossover_within_indv(individual):
            crossover_num = round(len(individual) * CONSTANT.PROB_MUTATE_CROSSOVER)
            if crossover_num % 2 == 1:
                crossover_num -= 1
            if crossover_num > 0:
                cross_rules = random.sample(individual, crossover_num)
                # individual = [rule for rule in individual if rule not in cross_rules]
                for i in range(int(crossover_num / 2)):
                    sub_crossover(cross_rules[i * 2], cross_rules[i * 2 + 1])
                    # individual += [child_1, child_2]

        def mutate_within_indv(individual):
            mutate_rule_num = int(len(individual) * CONSTANT.PROB_MUTATE_MUTATE)
            mutate_rules = random.sample(individual, mutate_rule_num)

            for rule in mutate_rules:
                mutate_index = random.randrange(4)
                if mutate_index == 0:
                    rule.ma_method = random.choice(CONSTANT.MA_METHODS)
                elif mutate_index == 1:
                    rule.l_s_values = random.choice(self.ma_combs)
                elif mutate_index == 2:
                    rule.fuzzy_extent = random.choice(CONSTANT.EXTENT)
                elif mutate_index == 3:
                    rule.rating_value = random.randint(-10, 10) / 10

        def my_mutate(individual):
            crossover_within_indv(individual)
            mutate_within_indv(individual)

        def get_rreturn(rlevel, datetime, row, cf, trans, dsl, rbl):
            cur_holding = int(CONSTANT.ORI_CAP_VALUE * rlevel / (row[CONSTANT.MA_DEFAULT_COL] * CONSTANT.DEPOSIT))
            pre_holding = 0 if cf.df.shape[0] == 0 else cf.df['holding'][cf.df.shape[0] - 1]
            if abs(cur_holding - pre_holding) >= CONSTANT.TRANS_THRESHOLD:
                tran = trans.insert(datetime=datetime, cur_holding=cur_holding, high=row['high'], low=row['low'])
                if tran['volume_s'][0] < 0:
                    dsl.insert(datetime=datetime, cost_borrow=tran['cost_borrow'][0], short_left=-tran['volume_s'][0], short_price=row['low'])
                elif tran['volume_s'][0] > 0:
                    ds_up_dict = dsl.update(tran)
                    rbl.insert(datetime=datetime, up_dict=ds_up_dict)
                rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl, tran=tran)
            else:
                rreturn = cf.insert(datetime=datetime, row=row, dsl=dsl)

            return rreturn

        def fitness(individual, data):
            rreturn = 0
            for rule in individual:
                diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                pre_diff = data[0][diff_col_name]
                # cur_diff = data[1][diff_col_name]
                # total_diff = pre_diff.append(cur_diff, ignore_index=True)
                # mf = MF(total_diff).get_mf()
                mf = MF(pre_diff).get_mf()
                rule.mf = mf

            cf = CapFlow(CapFlow.get_ori_df(data[1].index.values[0]))
            trans = Trans(Trans.get_empty_df())
            dsl = DymcShortList(DymcShortList.get_empty_df())
            rbl = ReturnBorrowLog(ReturnBorrowLog.get_empty_df())

            # for datetime, row in tqdm(data[1].iterrows()):
            for datetime, row in data[1].iterrows():
                rlevel = 0
                act = 0
                for rule in individual:
                    diff_col_name = "{}_{}_{}".format(rule.ma_method, rule.l_s_values[1], rule.l_s_values[0])
                    mfvalue = rule.mf(rule.fuzzy_extent, [row[diff_col_name]])
                    if mfvalue[0] > 0:
                        act += 1
                        rlevel += mfvalue[0] * rule.rating_value
                if act > 0:
                    rlevel /= act
                rreturn_t = get_rreturn(rlevel, datetime, row, cf, trans, dsl, rbl)
                rreturn += rreturn_t

            rreturn /= data[1].shape[0]
            return rreturn

        self.fitness_function = fitness
        self.create_individual = my_create_individual
        self.mutate_function = my_mutate

    def create_new_population(self):

        new_population = []
        for i in range(int(CONSTANT.POPULATION_BEST_PORTION * self.population_size)):
            elite = copy.deepcopy(self.current_generation[i])
            new_population.append(elite)

        selection = self.selection_function

        while len(new_population) < int(self.population_size * (CONSTANT.POPULATION_BEST_PORTION + CONSTANT.POPULATION_REMAIN_PORTION)):
            parent_1 = copy.deepcopy(selection(self.current_generation))
            parent_2 = copy.deepcopy(selection(self.current_generation))

            child_1, child_2 = parent_1, parent_2
            child_1.fitness, child_2.fitness = 0, 0

            can_crossover = random.random() < self.crossover_probability
            can_mutate = random.random() < self.mutation_probability

            if can_crossover:
                child_1.genes, child_2.genes = self.crossover_function(
                    parent_1.genes, parent_2.genes)

            if can_mutate:
                self.mutate_function(child_1.genes)
                self.mutate_function(child_2.genes)

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)

        remain_num = self.population_size - len(new_population)
        for i in range(remain_num):
            new_population.append(pyeasyga.Chromosome(self.create_individual(0)))

        self.current_generation = new_population

    def create_initial_population(self):

        initial_population = []
        if len(self.seed_data) > 2:
            initial_population.append(pyeasyga.Chromosome(self.seed_data[2]))

        while len(initial_population) < self.population_size:
            genes = self.create_individual(self.seed_data)
            individual = pyeasyga.Chromosome(genes)
            initial_population.append(individual)
        self.current_generation = initial_population