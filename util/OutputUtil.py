import pandas as pd
from entity import CONSTANT


class OutputUtil:

    @staticmethod
    def output_indv_list(filename, indv_tuple_list, final_population):

        df_all = pd.DataFrame(columns=['number', 'test_start', 'test_end', 'rate_of_return',
                                   'ma_method', 'comb', 'extent', 'rating_value'])
        df_best = pd.DataFrame(columns=['number', 'ma_method', 'comb', 'extent', 'rating_value'])
        df_result = pd.DataFrame()

        for i in range(len(indv_tuple_list)):
            for j in range(CONSTANT.NUM_OF_RULES_PER_INDV):
                data = {'number': [i],
                        'test_start': [indv_tuple_list[i][0]],
                        'test_end': [indv_tuple_list[i][1]],
                        'rate_of_return': [indv_tuple_list[i][2]],
                        'ma_method': [indv_tuple_list[i][3][j].ma_method],
                        'comb': [indv_tuple_list[i][3][j].l_s_values],
                        'extent': [indv_tuple_list[i][3][j].fuzzy_extent],
                        'rating_value': [indv_tuple_list[i][3][j].rating_value]}
                data_df = pd.DataFrame(data)
                df_all = df_all.append(data_df, ignore_index=True)
            df_result = df_result.append(indv_tuple_list[i][4])

        for i in range(len(final_population)):
            for j in range(len(final_population[i])):
                data = {'number': [i],
                        'ma_method': [final_population[i][j].ma_method],
                        'comb': [final_population[i][j].l_s_values],
                        'extent': [final_population[i][j].fuzzy_extent],
                        'rating_value': [final_population[i][j].rating_value]}
                data_df = pd.DataFrame(data)
                df_best = df_best.append(data_df, ignore_index=True)

        writer = pd.ExcelWriter(CONSTANT.OUTPUT_PATH + filename)
        df_all.to_excel(writer, 'all_best_individuals')
        df_best.to_excel(writer, 'best_individuals')
        df_result.to_excel(writer, 'results')
        writer.save()

    @staticmethod
    def output_process(filename, cf, trans, rbl):

        writer = pd.ExcelWriter(CONSTANT.OUTPUT_PATH + filename)
        cf.df.to_excel(writer, 'cap flow')
        trans.df.to_excel(writer, 'transactions')
        rbl.df.to_excel(writer, 'return borrow')
        writer.save()
