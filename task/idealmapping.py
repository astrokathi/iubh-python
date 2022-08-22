import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

from task.plot import Plot


class IdealMapping:

    def __init__(self):
        pass

    def map_ideal_function(self):
        pass

    def map_ideal_function(self, df_train: DataFrame = None, df_ideal: DataFrame = None, train_col: str = None,
                           plot=True) -> (float, str, float, float):
        """
        This method is to subtract df2 from df1 and store the deviation squared in a new dataframe
        :param df_train: Train dataframe
        :param df_ideal: Ideal dataframe
        :param train_col: training function for which the ideal mapping is being performed
        :param plot:
        :return:
        """
        df3 = pd.DataFrame()
        df_ideal_cols = df_ideal.columns
        feature_col = df_ideal_cols[0]

        # Sorting both  the dataframes based on the values of their x, this is an extra measure.
        df_train = df_train.sort_values(feature_col)
        df_ideal = df_ideal.sort_values(feature_col)

        df3[feature_col] = df_train[feature_col]

        for i in range(len(df_ideal.columns) - 1):
            y_value = df_ideal_cols[i + 1]
            df3[y_value] = (df_train[train_col] - df_ideal[y_value]) ** 2

        if plot:
            p = Plot()
            p.scatter_sub_plots_for_data(df=df3, row_num=10, col_num=5, theme="ggplot")
            plt.show()

        # The below function would return the mapped ideal function and the minimum least square sum value
        min_ideal_sum_value, min_ideal_sum_col_name = self.get_min_value_for_all_values_of_x(df3)

        # This is to evaluate the largest deviation between the training function and its mapped ideal function.
        largest_deviation_train_ideal, smallest_deviation_train_ideal = \
            self.largest_deviation_between_train_ideal(df_train=df_train,
                                                       df_ideal=df_ideal,
                                                       train_col=train_col,
                                                       mapped_ideal_col=min_ideal_sum_col_name)
        return min_ideal_sum_value, min_ideal_sum_col_name, largest_deviation_train_ideal, smallest_deviation_train_ideal

    @staticmethod
    def get_min_value_for_all_values_of_x(diff_df: DataFrame = None) -> (float, str):
        """
        diff_df is the deviation squared dataset
        :param diff_df: This is the dataframe with deviation squared values for each value in x
        :return: tuple of the minimum least squared value and the ideal column name for a given training function
        """

        """
        we will now sum, all the rows to add up all values a function for all the value of x
        Then append it to the dataframe diff_df in the end, axis=1 represents summation amongst the rows and a new
        column is created
        """
        diff_df.loc[len(diff_df)] = diff_df.sum(axis=0)
        last_index = len(diff_df) - 1

        """
        The minimum value amongst the functions after summation is
        """
        min_ideal_sum_value = diff_df.iloc[:, 1:].min(axis=1).loc[last_index]
        min_ideal_sum_col_name = diff_df.iloc[:, 1:].idxmin(axis=1).loc[last_index]
        return min_ideal_sum_value, min_ideal_sum_col_name

    @staticmethod
    def largest_deviation_between_train_ideal(df_train=None, df_ideal=None,
                                              train_col=None, mapped_ideal_col=None) -> float:
        ideal_y_val = df_ideal[mapped_ideal_col]
        train_y_val = df_train[train_col]

        large_dev_df = pd.concat([ideal_y_val, train_y_val], axis=1)
        """
        Finding the deviation square in a dataframe between two columns and storing it in a new column.
        Here the least squared is chosen to make it align with calculation involved during the evaluation of the
        mapping functions.
        """
        large_dev_df['y_dev'] = (large_dev_df[train_col] - large_dev_df[mapped_ideal_col]) ** 2
        # Taking the max of the column y_dev to get the largest deviation possible
        return large_dev_df.max(axis=0)['y_dev'], large_dev_df.min(axis=0)['y_dev']
