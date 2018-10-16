import math
import numpy as np
import scipy.stats as stats
from entity import CONSTANT

class MF:


    def __init__(self, diff_series):
        self.diff_series = diff_series

    def get_mf(self):
        sorted_diff = self.diff_series
        count_per_group = math.floor(len(self.diff_series) / CONSTANT.EXTENT_GROUPS)
        mod = len(self.diff_series) % CONSTANT.EXTENT_GROUPS

        extent_groups = []
        for i in range(0, CONSTANT.EXTENT_GROUPS):
            if i <= mod - 1:
                extent_groups.append(sorted_diff[:count_per_group + 1])
                sorted_diff = sorted_diff.drop(sorted_diff.index[:count_per_group + 1])
                sorted_diff.reset_index(inplace=True, drop=True)
            else:
                extent_groups.append(sorted_diff[:count_per_group])
                sorted_diff = sorted_diff.drop(sorted_diff.index[:count_per_group])
                sorted_diff.reset_index(inplace=True, drop=True)

        parameters = []
        maximum = []
        for i in range(0, len(extent_groups)):
            samples = np.array(extent_groups[i])
            param, maxi = self.get_parameters_maximum(samples)
            parameters.append(param)
            maximum.append(maxi)

        def mf(extent, diff):
            value = self.get_membership_grade(diff, parameters[extent], maximum[extent])
            return value

        return mf

    # normal distribution fit
    def get_parameters_maximum(self, train):
        parameters = stats.norm.fit(train)
        maximum = max(stats.norm.pdf(train, *parameters))
        return parameters, maximum

    def get_membership_grade(self, value, parameters, maximum):
        return stats.norm.pdf(value, *parameters) / maximum