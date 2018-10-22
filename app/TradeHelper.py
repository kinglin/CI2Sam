from entity import CONSTANT
from queue import PriorityQueue
import copy
from ga.myga import myga
from ga.myga4trade import myga4trade
from ga.apply2test import apply2test
from capflow.CapFlow import CapFlow
from capflow.DymcShortList import DymcShortList
from capflow.DymcShortList import ReturnBorrowLog
from capflow.Trans import Trans
from util.OutputUtil import OutputUtil
import time
from tqdm import tqdm


class TradeHelper:

    def __init__(self, raw_data_ma_diffs, train_groups, selection_groups, test_groups):
        self.raw_data_ma_diffs = raw_data_ma_diffs
        self.train_groups = train_groups
        self.selection_groups = selection_groups
        self.test_groups = test_groups
        pass

    def get_best_individuals(self):

        best_indv_queue = PriorityQueue()
        best_indv_list = list()

        cf = CapFlow(CapFlow.get_ori_df(self.test_groups[1][0]))
        trans = Trans(Trans.get_empty_df())
        dsl = DymcShortList(DymcShortList.get_empty_df())
        rbl = ReturnBorrowLog(ReturnBorrowLog.get_empty_df())

        # loop for each group(except the first one, because it doesn't have previous one)
        for group_index in range(1, len(self.train_groups)):
            start_time = time.time()
            print('=====group index: {}/{}====='.format(group_index, len(self.train_groups)))
            best_individual_in_train = self.get_best_indv_in_train(group_index)
            # print('==train end==')
            best_individual_in_selection = self.get_best_indv_in_selection(group_index, best_individual_in_train)
            # print('==selection end==')
            rate_of_return = self.get_rreturn_from_test(group_index=group_index,
                                                        indvidual=best_individual_in_selection,
                                                        cf=cf, trans=trans, dsl=dsl, rbl=rbl)
            # print('==test end==')
            best_indv_queue.put((-rate_of_return, copy.deepcopy(best_individual_in_selection)))

            test_index_list = self.test_groups[group_index]
            test_start = str(test_index_list[0])
            test_end = str(test_index_list[len(test_index_list) - 1])
            best_indv_list.append((test_start, test_end, rate_of_return, best_individual_in_selection, copy.deepcopy(cf.df[-1:])))
            end_time = time.time()
            print('=====group index: {}/{}  {}s  {}====='.format(group_index, len(self.train_groups), end_time - start_time, rate_of_return))

        final_population = self.get_best_indvs(best_indv_queue, CONSTANT.NUM_OF_POPULATION)

        OutputUtil.output_indv_list("{}_{}.xlsx".format('best_individuals_of_simulation', str(CONSTANT.TRANS_THRESHOLD))
                                    , best_indv_list, final_population)
        OutputUtil.output_process("{}_{}.xlsx".format('total_process_of_simulation', str(CONSTANT.TRANS_THRESHOLD))
                                  , cf=cf, trans=trans, rbl=rbl)

        return final_population

    def get_total_test_profit(self, individuals):

        best_indv_queue = PriorityQueue()
        best_indv_list = list()

        print(len(self.train_groups))

        cf = CapFlow(CapFlow.get_ori_df(self.test_groups[1][0]))
        trans = Trans(Trans.get_empty_df())
        dsl = DymcShortList(DymcShortList.get_empty_df())
        rbl = ReturnBorrowLog(ReturnBorrowLog.get_empty_df())

        # loop for each group(except the first one, because it doesn't have previous one)
        for group_index in range(1, len(self.train_groups)):
            start_time = time.time()
            print('=====group index: {}/{}====='.format(group_index, len(self.train_groups)))
            best_individual_in_train = self.get_best_indv_in_train_trade(group_index, individuals)
            # print('==train end==')
            best_individual_in_selection = self.get_best_indv_in_selection(group_index, best_individual_in_train)
            # print('==selection end==')
            rate_of_return = self.get_rreturn_from_test(group_index=group_index,
                                                        indvidual=best_individual_in_selection,
                                                        cf=cf, trans=trans, dsl=dsl, rbl=rbl)
            # print('==test end==')
            best_indv_queue.put((-rate_of_return, copy.deepcopy(best_individual_in_selection)))

            test_index_list = self.test_groups[group_index]
            test_start = str(test_index_list[0])
            test_end = str(test_index_list[len(test_index_list) - 1])
            best_indv_list.append((test_start, test_end, rate_of_return, best_individual_in_selection, copy.deepcopy(cf.df[-1:])))
            end_time = time.time()
            print('=====group index: {}/{}  {}s  {}====='.format(group_index, len(self.train_groups), end_time - start_time, rate_of_return))

        final_population = self.get_best_indvs(best_indv_queue, CONSTANT.NUM_OF_POPULATION)

        OutputUtil.output_indv_list("{}_{}.xlsx".format('best_individuals', str(CONSTANT.TRANS_THRESHOLD))
                                    , best_indv_list, final_population)
        OutputUtil.output_process("{}_{}.xlsx".format('total_process', str(CONSTANT.TRANS_THRESHOLD))
                                  , cf=cf, trans=trans, rbl=rbl)

        return cf.df[-1:]

    def get_best_indv_in_train_trade(self, group_index, individuals):
        seed_data = self.form_seed_data_4_train_trade(self.train_groups[group_index - 1],
                                                      self.train_groups[group_index], individuals)
        ga = myga4trade(seed_data,
                  population_size=CONSTANT.NUM_OF_POPULATION,
                  generations=1,
                  crossover_probability=CONSTANT.PROB_CROSSOVER,
                  mutation_probability=CONSTANT.PROB_MUTATE,
                  elitism=True,
                  maximise_fitness=True)
        ga.run()
        return ga.best_individual()[1]

    def get_best_indv_in_train(self, group_index):
        seed_data = self.form_seed_data_4_train(self.train_groups[group_index - 1], self.train_groups[group_index])
        ga = myga(seed_data,
                    population_size=CONSTANT.NUM_OF_POPULATION,
                    generations=1,
                    crossover_probability=CONSTANT.PROB_CROSSOVER,
                    mutation_probability=CONSTANT.PROB_MUTATE,
                    elitism=True,
                    maximise_fitness=True)
        ga.run()
        return ga.best_individual()[1]

    def get_best_indv_in_selection(self, group_index, best_individual_in_train):
        seed_data = self.form_seed_data_4_selection(self.selection_groups[group_index - 1],
                                                    self.selection_groups[group_index],
                                                    best_individual_in_train)
        ga = myga(seed_data,
                        population_size=CONSTANT.NUM_OF_POPULATION,
                        generations=CONSTANT.NUM_OF_GENERATION,
                        crossover_probability=CONSTANT.PROB_CROSSOVER,
                        mutation_probability=CONSTANT.PROB_MUTATE,
                        elitism=True,
                        maximise_fitness=True)

        ga.run()
        return ga.best_individual()[1]

    def get_rreturn_from_test(self, group_index, indvidual, cf, trans, dsl, rbl):

        index_list = self.test_groups[group_index]
        data = self.raw_data_ma_diffs.loc[str(index_list[0]):str(index_list[len(index_list) - 1])]
        rreturn = apply2test(data, indvidual, cf, trans, dsl, rbl).fitness()

        return rreturn

    def form_seed_data_4_train(self, list1, list2):

        pre_data = self.raw_data_ma_diffs.loc[str(list1[0]):str(list1[len(list1) - 1])]
        cur_data = self.raw_data_ma_diffs.loc[str(list2[0]):str(list2[len(list2) - 1])]

        return pre_data, cur_data

    def form_seed_data_4_selection(self, list1, list2, ori_indv):

        pre_data = self.raw_data_ma_diffs.loc[str(list1[0]):str(list1[len(list1) - 1])]
        cur_data = self.raw_data_ma_diffs.loc[str(list2[0]):str(list2[len(list2) - 1])]

        return pre_data, cur_data, ori_indv

    def form_seed_data_4_train_trade(self, list1, list2, indvs):

        pre_data = self.raw_data_ma_diffs.loc[str(list1[0]):str(list1[len(list1) - 1])]
        cur_data = self.raw_data_ma_diffs.loc[str(list2[0]):str(list2[len(list2) - 1])]

        return pre_data, cur_data, indvs

    def get_best_indvs(self, pri_queue, num):
        i = 0
        items = []
        while i < num:
            if pri_queue.empty():
                break
            items.append(pri_queue.get()[1])
            i += 1
        return items
