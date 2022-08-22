"""
These are the block comments about the Test class
In this we will analyze the numpy, pandas and other libraries for understanding the data
"""
import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def load_csv_as_data(file_name=None):
    return pd.read_csv(file_name)


class Test:

    def load_train_data(self):
        current_dir = os.path.curdir
        train_file_path = os.path.join(current_dir, "../resources/train.csv")
        return load_csv_as_data(train_file_path)

    def load_ideal_data(self):
        current_dir = os.path.curdir
        ideal_file_path = os.path.join(current_dir, "../resources/ideal.csv")
        return load_csv_as_data(ideal_file_path)

    def load_test_data(self):
        current_dir = os.path.curdir
        test_file_path = os.path.join(current_dir, "../resources/test.csv")
        return load_csv_as_data(test_file_path)

    def test_kwargs(self, **kwargs):
        """
        The kwargs will be a dictionary and it can be used to fetch certain values based on the keys and then
        we can process the arguments that are passed.
        :param kwargs:
        :return:
        """
        print(kwargs.get("theme"))

    def scatter_sub_plots_for_data(self, df=None, row_num=None, col_num=None, theme=None):
        theme_value = 'default'
        if theme is not None:
            theme_value = theme
        matplotlib.style.use(theme_value)

        """
        Plotting the actual data starts by collecting the row and col count and dataframe itself
        fig, ax for subplots where ax will be a tuple with the shape as row_num , col_num
        """
        fig, ax = plt.subplots(row_num, col_num)

        """
        To plot y1,y2,y3 and y4, the counter should start from 1 through 4
        """
        count = 1

        for i in range(row_num):
            for j in range(col_num):
                y_value = 'y'
                y_value = y_value + str(count)
                df.plot.scatter(x='x', y=y_value, ax=ax[i, j])
                count = count + 1
        plt.show()

    def sub_series_from_two_dataframes(self, df1=None, df2=None, col1=None, col2=None, plot=True):
        df3 = pd.DataFrame()
        """
        Sorting both  the dataframes based on the values of their x, this is an extra measure.
        """
        df1 = df1.sort_values('x')
        df2 = df2.sort_values('x')

        """
        These are not needed now, as there are analysed and found out that the x are same for the training and the ideal
        function.
        """
        # df3['x1'] = df1['x']
        # df3['x2'] = df2['x']
        # df3['xdiff'] = (df1.x - df2.x) ** 2
        df3['x'] = df1['x']
        for i in range(len(df2.columns) - 1):
            y_value = 'y' + str(i + 1)
            df3[y_value] = (df1[col1] - df2[y_value]) ** 2

        if plot:
            self.scatter_sub_plots_for_data(df=df3, row_num=10, col_num=5, theme="ggplot")
            plt.show()
        return df3

    def get_min_value_for_all_values_of_x(self, diff_df=None):
        """
        diff_df is the deviation squared dataset.(400 X 51)
        :param diff_df:
        :return:
        """

        """
        we will now sum, all the rows to add up all values a function for all the value of x
        Then append it to the dataframe diff_df in the end, axis=1 represents summation amongst the rows.
        """
        diff_df.loc[len(diff_df)] = diff_df.sum(axis=0)
        last_index = len(diff_df) - 1

        """
        The minimum value amongst the functions after summation is
        """
        min_ideal_sum_value = diff_df.iloc[:, 1:].min(axis=1).loc[last_index]
        min_ideal_sum_col_name = diff_df.iloc[:, 1:].idxmin(axis=1).loc[last_index]
        return min_ideal_sum_value, min_ideal_sum_col_name

    def polynomial_regression_on_train_data(self, train_df=None, train_col_name=None, plot_curve=True):
        reg_model = LinearRegression()
        poly = PolynomialFeatures(degree=(1, 12), include_bias=False)

        x_reg_train = train_df['x'].values.reshape(len(train_df), 1)
        y_reg_train = train_df[train_col_name].values.reshape(len(train_df), 1)

        poly_features = poly.fit_transform(x_reg_train)

        reg_model.fit(poly_features, y_reg_train)
        if plot_curve:
            plt.scatter(x_reg_train, y_reg_train, color='black')
            plt.plot(x_reg_train, reg_model.predict(poly_features), color='blue', linewidth=2)
            plt.show()
        # print(reg_model.predict(test_df['x'].values.reshape(len(test_df), 1)))
        return reg_model, poly


if __name__ == "__main__":
    """
    This is to list all the available plot styles in matplotlib
    """
    global_test = pd.DataFrame()
    global_dict_train = dict()
    print(plt.style.available)
    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True

    t = Test()
    data_frame_train = t.load_train_data()
    # t.scatter_sub_plots_for_data(df=data_frame_train, theme='seaborn', row_num=2, col_num=2)
    data_frame_test = t.load_test_data()
    global_test = data_frame_test
    # print("Checking how the test data looks like", data_frame_test.head())
    data_frame_ideal = t.load_ideal_data()
    # print("The shape of the ideal dataframe is", data_frame_ideal.shape)
    # t.scatter_sub_plots_for_data(df=data_frame_ideal, theme='fast', row_num=10, col_num=5)
    # t.test_kwargs(df=data_frame_ideal, theme='fast', row_num=10, col_num=5)

    for i in range(1, 5):
        y_var = 'y' + str(i)


        (poly_model, poly_transform) = t.polynomial_regression_on_train_data(train_df=data_frame_train,
                                                                             train_col_name=y_var, plot_curve=False)
        updated_df = t.sub_series_from_two_dataframes(df1=data_frame_train, df2=data_frame_ideal, col1=y_var,
                                                      plot=False)

        # print("Analysing the newly constructed dataframe", diff_df.head())

        (min_ideal_val, min_ideal_col) = t.get_min_value_for_all_values_of_x(diff_df=updated_df)

        # print("The minimum summation value for function {} is {}".format(min_ideal_col, min_ideal_val))

        # print("The ideal function is {} for the actual function {}".format(min_ideal_col, y_var))

        ideal_y_val = data_frame_ideal[min_ideal_col]
        train_y_val = data_frame_train[y_var]

        """
        creating a new dataframe to calculate the largest deviation from ideal and train y values.
        now, we subtract them and square them and take square root to get the rms value.
        """
        large_dev_df = pd.concat([ideal_y_val, train_y_val], axis=1)
        large_dev_df['y_dev'] = np.sqrt((large_dev_df[min_ideal_col] - large_dev_df[y_var]) ** 2)
        # print("The largest deviation between ideal function {} and train function {} is {}".format(min_ideal_col, y_var, large_dev_df.max(axis=0)['y_dev']*sqrt(2)))

        global_dict_train[y_var] = {"ideal": min_ideal_col, "ideal_min": min_ideal_val, "train": y_var,
                                    "largest_dev": large_dev_df.max(axis=0)['y_dev'] * sqrt(2)}

        x_test = data_frame_test['x'].values.reshape(len(data_frame_test), 1)
        y_test_predicted = poly_model.predict(poly_transform.fit_transform(x_test))
        global_test[y_var] = pd.Series(y_test_predicted.reshape(len(y_test_predicted[:]), ), name=y_var)
        # global_test[y_var] = pd.Series(y_test_predicted)

    for i in range(1, 5):
        y_pred_var = 'y' + str(i)
        global_test[y_pred_var] = np.sqrt((global_test[y_pred_var] - global_test['y']) ** 2)

    """
    taking the max from rows 2 through 5 from the global_test dataframe,
    here do we need to take max or min, If we consider max then most of them are exceeding.
    """
    global_test['y_test_dev'] = global_test.iloc[:, 2:6].max(axis=1)

    # print(global_test.iloc[0]['y1'])
    global_test['results'] = np.nan
    global_test['results'].fillna('', inplace=True)
    global_dic = dict()
    for key in global_dict_train.keys():
        obj = global_dict_train[key]
        obj['largest_dev']
        for l in range(len(global_test)):
            if global_test.iloc[l]['y_test_dev'] <= obj['largest_dev']:
                try:
                    global_dic[l] = global_dic[l] + obj['ideal'] + ','
                except KeyError:
                    global_dic[l] = ''
                    global_dic[l] = global_dic[l] + obj['ideal'] + ','
                # global_test.loc[l].results.copy = obj['ideal'] + ','
            else:
                # global_test.loc[l].results = ''
                try:
                    global_dic[l] = global_dic[l] + ''
                except KeyError:
                    global_dic[l] = ''
                    global_dic[l] = global_dic[l] + ''
    print(global_dic)
    print(global_test.head())
    print(global_dict_train)
    """
    In the Test dataset the (x,y) points are provided.
    Take only x and find 4 y values as per the y1, y2, y3 and y4 training data, using regression.
    once we get all the y values, consider the max deviation -> sqrt(difference**2)
    This value let us say max_dev
    lar_dev1, lar_dev2, lar_dev3, lar_dev4
    max_dev <= either of (lar_dev1 | lar_dev2 | lar_dev3 | lar_dev4)*√2
    evaluate how many of them you can find from these chosen 4.
    """
