from datetime import date


class DataHelper:
    # UNIT_MINUTE = "minute"
    # GROUP_15 = 15
    TRADE_DATE = date(2014, 1, 2)
    DIV_30 = 30

    # RATIO = 6
    # DAYS_PER_DIV = 120  # 1 quarter per division

    # data is raw data, pandas dataframe
    def __init__(self, data, days_per_div):
        self.data = data
        self.days_per_div = days_per_div
        self.unique_dates = sorted(set(self.data.index.date))
        # self.group_number = group_number

    # return previous n_days' dates from target
    def find_previous_dates(self, unique_dates, target, n_days):
        for i in range(0, len(unique_dates)):
            if unique_dates[i] == target:
                index = i
                break

        n_days_list = []
        for i in range(1, n_days + 1):
            if index - i >= 0:
                n_days_list.append(unique_dates[index - i])
            else:
                break
        return sorted(n_days_list)

    # return n_days' dates from target (containing target)
    def find_containing_dates(self, unique_dates, target, n_days):
        for i in range(0, len(unique_dates)):
            if unique_dates[i] == target:
                index = i
                break

        n_days_list = []
        for i in range(0, n_days):
            if index + i < len(unique_dates):
                n_days_list.append(unique_dates[index + i])
            else:
                break
        return sorted(n_days_list)

    # return next day's date of target
    def find_next_date(self, unique_dates, target):
        n_days = 2
        for i in range(0, len(unique_dates)):
            if unique_dates[i] == target:
                index = i
                break

        n_days_list = []
        for i in range(0, n_days):
            if index + i < len(unique_dates):
                n_days_list.append(unique_dates[index + i])
            else:
                break
        return sorted(n_days_list)[-1]

    # return yesterday's date of target
    def find_yesterday_date(self, unique_dates, target):
        n_days = 1
        for i in range(0, len(unique_dates)):
            if unique_dates[i] == target:
                index = i
                break

        n_days_list = []
        for i in range(1, n_days + 1):
            if index - i >= 0:
                n_days_list.append(unique_dates[index - i])
            else:
                break
        return sorted(n_days_list)[0]

    #########
    def get_unique_dates(self):
        print(self.unique_dates)

    def get_data_groups(self):
        # deal with self.data and return a list
        # every element is a dataframe

        B_days = len(set(self.data.loc[str(self.TRADE_DATE):].index.date))
        B_divs = round(B_days / self.days_per_div)

        target = self.TRADE_DATE
        temp_divB_groups = []

        for i in range(0, B_divs):
            temp_divB_groups.append(self.find_containing_dates(self.unique_dates, target, self.days_per_div))
            target = self.find_next_date(self.unique_dates, temp_divB_groups[-1][-1])

        A_days = len(set(self.data.loc[:str(self.find_yesterday_date(self.unique_dates, self.TRADE_DATE))].index.date))
        A_divs = round(A_days / self.days_per_div)

        target = self.TRADE_DATE
        temp_divA_groups = []
        for i in range(0, A_divs):
            temp_divA_groups.append(self.find_previous_dates(self.unique_dates, target, self.days_per_div))
            target = temp_divA_groups[-1][0]
        temp_divA_groups.reverse()

        temp_divA_groups.pop(0)  # discard first group from divA
        total_div = len(temp_divA_groups) + len(temp_divB_groups)
        train_div_size = 2
        selection_div_size = 1
        test_div_size = 1
        group_length = train_div_size + test_div_size

        total_groups = total_div - group_length + 1

        total_div_groups = temp_divA_groups + temp_divB_groups
        trade_group_index = len(temp_divA_groups)

        train_groups = []
        selection_groups = []
        test_groups = []
        for i in range(0, total_groups):
            train_groups.append(total_div_groups[i] + total_div_groups[i + 1])
            selection_groups.append(total_div_groups[i + 1])
            test_groups.append(total_div_groups[i + 2])
            if i + 2 == trade_group_index:
                trade_in_test_index = len(test_groups) - 1

        #         train_groups, selection_groups, test_groups, trade_index = [], [], [], 3
        return train_groups, selection_groups, test_groups, trade_in_test_index
