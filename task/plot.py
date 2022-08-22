import matplotlib.pyplot as plt
import matplotlib
from pandas import DataFrame


class Plot:

    def __init__(self):
        pass

    @staticmethod
    def scatter_sub_plots_for_data(df: DataFrame = None, row_num: int = None, col_num: int = None,
                                   theme: str = None):
        """
        This is to plot the subplots of a dataframe, df. The row_num and col_num creates a grid of subplots.
        The scatter plot will be created for each column starting with index 0 as x-axis and the index 1 through n on
        the y-axis.
        Theme value can be a style for which the plot can be shown.
        If the theme mentioned is not registered, default theme will be applied.
        :param df:
        :param row_num:
        :param col_num:
        :param theme:
        :return:
        """

        theme_value = 'default'
        if theme is not None:
            theme_value = theme
        matplotlib.style.use(theme_value)

        """
        Plotting the actual data starts by collecting the row and col count and dataframe itself
        fig, ax for subplots where ax will be a tuple with the shape as row_num , col_num
        """
        fig, ax = plt.subplots(row_num, col_num)

        count = 1
        columns = df.columns
        for i in range(row_num):
            for j in range(col_num):
                df.plot.scatter(x=columns[0], y=columns[count], ax=ax[i, j])
                count = count + 1
        plt.show()
