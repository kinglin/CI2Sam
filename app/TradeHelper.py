from entity.Individual import Individual
from ga.myga4train import myga4train
from entity import CONSTANT
from queue import PriorityQueue
import copy

class TradeHelper:

    def __init__(self, raw_data_ma_diffs, train_groups, selection_groups, test_groups):
        self.raw_data_ma_diffs = raw_data_ma_diffs
        self.train_groups = train_groups
        self.selection_groups = selection_groups
        self.test_groups = test_groups
        pass

    def get_best_individuals(self):

        best_indv_queue = PriorityQueue()

        # loop for each group(except the first one, because it doesn't have previous one)
        for group_index in range(1, len(self.train_groups)):
            best_individual_in_train = self.get_best_indv_in_train(group_index)
            best_individual_in_selection = self.get_best_indv_in_selection(group_index, best_individual_in_train)
            rate_of_return = self.get_rreturn_from_test(best_individual_in_selection)
            best_indv_queue.put((-rate_of_return, copy.deepcopy(best_individual_in_selection)))

        final_population = self.get_best_indvs(best_indv_queue, CONSTANT.NUM_OF_POPULATION)

        return final_population

    def get_total_test_profit(self, individual):
        profit = 0
        return profit

    def get_best_indv_in_train(self, group_index):
        seed_data = self.form_seed_data_4_train(self.train_groups[group_index - 1], self.train_groups[group_index])
        ga = myga4train(seed_data,
                        population_size=CONSTANT.NUM_OF_POPULATION,
                        generations=1,
                        crossover_probability=CONSTANT.PROB_CROSSOVER,
                        mutation_probability=CONSTANT.PROB_MUTATE,
                        elitism=True,
                        maximise_fitness=True)
        ga.fitness_function = self.fitness
        ga.run()
        return ga.best_individual()

    def get_best_indv_in_selection(self, group_index, best_individual_in_train):
        seed_data = self.form_seed_data_4_selection(self.selection_groups[group_index - 1],
                                                    self.selection_groups[group_index],
                                                    best_individual_in_train)
        ga = myga4train(seed_data,
                        population_size=CONSTANT.NUM_OF_POPULATION,
                        generations=CONSTANT.NUM_OF_GENERATION,
                        crossover_probability=CONSTANT.PROB_CROSSOVER,
                        mutation_probability=CONSTANT.PROB_MUTATE,
                        elitism=True,
                        maximise_fitness=True)
        ga.fitness_function = self.fitness
        ga.run()
        return ga.best_individual()

    def get_rreturn_from_test(self, indv):
        return 0

    def form_seed_data_4_train(self, list1, list2):
        return []

    def form_seed_data_4_selection(self, list1, list2, ori_indv):
        return []

    def form_seed_data_4_test(self, list1, list2):
        return []

    def fitness(self, individual, data):
        return 0

    def get_best_indvs(self, pri_queue, num):
        i = 0
        items = []
        while i < num:
            if pri_queue.empty():
                break
            items.append(pri_queue.get()[1])
            i += 1
        return items
