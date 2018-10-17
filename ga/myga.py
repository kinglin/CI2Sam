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

        def my_mutate(individual):
            mutate_index = random.randrange(len(individual))
            individual[mutate_index] = (0, 1)[individual[mutate_index] == 0]

        self.fitness_function = None
        self.create_individual = my_create_individual
        self.mutate_function = my_mutate



    def create_new_population(self):

        pass

    def create_initial_population(self):
        pass
