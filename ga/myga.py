from pyeasyga import pyeasyga
from entity.MA import MA
import random
from entity.Rule import Rule
from entity import CONSTANT


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
            for _ in range(self.population_size):
                rule = Rule(random.choice(CONSTANT.MA_METHODS),
                            random.choice(self.ma_combs),
                            random.choice(CONSTANT.EXTENT),
                            random.randint(-10, 10) / 10)
                rules.append(rule)

            return rules

        def sub_crossover(parent_1, parent_2):
            index = random.randrange(1, len(parent_1))
            child_1 = parent_1[:index] + parent_2[index:]
            child_2 = parent_2[:index] + parent_1[index:]
            return child_1, child_2

        def crossover_within_indv(individual):
            crossover_num = round(len(individual) * CONSTANT.PROB_MUTATE_CROSSOVER)
            if crossover_num % 2 == 1:
                crossover_num -= 1
            if crossover_num > 0:
                cross_rules = random.sample(individual, crossover_num)
                individual = [rule for rule in individual if rule not in cross_rules]
                for i in range(int(crossover_num / 2)):
                    child_1, child_2 = sub_crossover(cross_rules[i * 2], cross_rules[i * 2 + 1])
                    individual += [child_1, child_2]

        def mutate_within_indv(individual):
            mutate_rule_num = int(len(individual) * CONSTANT.PROB_MUTATE_MUTATE)
            mutate_rules = random.sample(individual, mutate_rule_num)

            for rule in mutate_rules:
                mutate_index = random.randrange(len(rule))
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

        self.fitness_function = None
        self.create_individual = my_create_individual
        self.mutate_function = my_mutate

    def create_new_population(self):

        pass
