import math
import numpy as np
import scipy.stats as stats

class MF:
    EXTENT_GROUPS = 7

    def __init__(self, diff_series):
        self.diff_series = diff_series

    def get_mf(self):
        sorted_diff = self.diff_series

        len_extent_group_A = math.floor(self.EXTENT_GROUPS / 2)
        len_extent_group_B = len_extent_group_A

        group_A = sorted_diff.loc[sorted_diff < 0]
        group_B = sorted_diff.loc[sorted_diff >= 0]
        group_B.reset_index(inplace=True, drop=True)

        count_per_group_A = math.floor(len(group_A) / len_extent_group_A)
        mod_A = len(group_A) % len_extent_group_A
        # count_per_group_A, mod_A

        count_per_group_B = math.floor(len(group_B) / len_extent_group_B)
        mod_B = len(group_B) % len_extent_group_B
        # count_per_group_B, mod_B

        extent_groups_A = []
        if count_per_group_A != 0:
            for i in range(0, len_extent_group_A):
                if i <= mod_A - 1:
                    extent_groups_A.append(group_A[:count_per_group_A + 1])
                    group_A = group_A.drop(group_A.index[:count_per_group_A + 1])
                    group_A.reset_index(inplace=True, drop=True)
                else:
                    extent_groups_A.append(group_A[:count_per_group_A])
                    group_A = group_A.drop(group_A.index[:count_per_group_A])
                    group_A.reset_index(inplace=True, drop=True)

        extent_groups_B = []
        if count_per_group_B != 0:
            for i in range(0, len_extent_group_B):
                if i <= mod_B - 1:
                    extent_groups_B.append(group_B[:count_per_group_B + 1])
                    group_B = group_B.drop(group_B.index[:count_per_group_B + 1])
                    group_B.reset_index(inplace=True, drop=True)
                else:
                    extent_groups_B.append(group_B[:count_per_group_B])
                    group_B = group_B.drop(group_B.index[:count_per_group_B])
                    group_B.reset_index(inplace=True, drop=True)

        points = self.get_points(extent_groups_A, extent_groups_B)

        def mf(extent, diff):
            value = self.get_membership_grade(diff, extent, points)
            return value

        return mf

    def get_points(self, extent_groups_A, extent_groups_B):
        points = []
        if len(extent_groups_A) == 0:
            points.append(-3)
            points.append(-2)
            points.append(-1)
        else:
            for group in extent_groups_A:
                points.append(min(group))
        points.append(0)
        if len(extent_groups_B) == 0:
            points.append(1)
            points.append(2)
            points.append(3)
        else:
            for group in extent_groups_B:
                points.append(max(group))
        return points

    # values is a list of values
    # return is a list of results
    def get_membership_grade(self, values, extent, points):

        if extent == 'EL':
            diff = abs(points[0] - points[1])
            point1 = points[0] - diff
            point2 = points[0]
            point3 = points[1]

            x = np.array([point1, point2, point3])
            y = np.array([0, 1, 0])
            eqn = np.poly1d(np.polyfit(x, y, 2))

            result = []
            for value in values:
                if value <= points[0]:
                    result.append(1)
                elif value >= points[1]:
                    result.append(0)
                else:
                    result.append(eqn(value))

        elif (extent == 'VL') | (extent == 'L') | (extent == 'M') | (extent == 'H') | (extent == 'VH'):
            if (extent == 'VL'):
                i = 0
            elif (extent == 'L'):
                i = 1
            elif (extent == 'M'):
                i = 2
            elif (extent == 'H'):
                i = 3
            else:
                i = 4
            point1a = points[i]
            point2a = points[i + 1]
            diff = abs(points[i] - points[i + 1])
            point3a = points[i + 1] + diff

            x_a = np.array([point1a, point2a, point3a])
            y_a = np.array([0, 1, 0])
            eqn_a = np.poly1d(np.polyfit(x_a, y_a, 2))

            diff = abs(points[i + 1] - points[i + 2])
            point1b = points[i + 1] - diff
            point2b = points[i + 1]
            point3b = points[i + 2]

            x_b = np.array([point1b, point2b, point3b])
            y_b = np.array([0, 1, 0])
            eqn_b = np.poly1d(np.polyfit(x_b, y_b, 2))

            result = []
            for value in values:
                if value <= points[i]:
                    result.append(0)
                elif value >= points[i + 2]:
                    result.append(0)
                elif (value > points[i]) & (value < points[i + 1]):
                    result.append(eqn_a(value))
                else:
                    result.append(eqn_b(value))

        elif extent == 'EH':
            point1 = points[5]
            point2 = points[6]
            diff = abs(points[5] - points[6])
            point3 = points[6] + diff

            x = np.array([point1, point2, point3])
            y = np.array([0, 1, 0])
            eqn = np.poly1d(np.polyfit(x, y, 2))

            result = []
            for value in values:
                if value <= points[5]:
                    result.append(0)
                elif value >= points[6]:
                    result.append(1)
                else:
                    result.append(eqn(value))

        return result