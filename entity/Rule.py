class Rule:

    def __init__(self, ma_method, l_s_values, fuzzy_extent, rating_value, mf=None):
        self.ma_method = ma_method
        self.l_s_values = l_s_values
        self.fuzzy_extent = fuzzy_extent
        self.rating_value = rating_value
        self.mf = mf
