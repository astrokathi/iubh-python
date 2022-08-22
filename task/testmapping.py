class TestMapping:

    def __init__(self):
        pass

    def predict_test_values_and_store_max_deviation(self, test_data=None, poly_dict=None):
        """
        This method is used to calculate the predicted values for each training functions and take the max values among
        those regression values and store it in a new column in the 'delta_y' in the test_data dataframe
        :param test_data: test_data is the loaded csv as a dataframe
        :param poly_dict: This holds the polynomial transformer and linear regression model for each training function.
        :return: This returns the modified test_data with added columns as delta_y which stores max deviation
        """

        if test_data is None:
            raise ValueError({"message": "The test data can't be empty", "data": None})

        if poly_dict is None:
            raise ValueError({"message": "The polynomial regression models and transformers are empty", "data": None})
        # predicting the test values
        x_val = test_data['x']
        y_val = test_data['y']

        # For each x,y test pair, the value for the feature x can be predicted using 4 different training models.
        # The predicted values will be evaluated to calculate the deviation and then check for the condition.
        # to find out the mapped ideal function
        for idx, pol in poly_dict.items():
            # transform the x value using the transformer
            x_trans_val = pol["transformer"].fit_transform(x_val.values.reshape(len(test_data), 1))

            # predict the y val using the poly model for the given x value.
            y_pred_val = pol["model"].predict(x_trans_val)

            # converting the values to series from nd array
            y_pred_val_series = y_pred_val.reshape(len(y_pred_val), )

            # Calculating the delta values
            # The delta is calculated in such a way that it aligns with others deviations so, we consider -
            # - deviation squared.
            test_data[idx] = (y_pred_val_series - y_val) ** 2

        # print(test_data.head())
        # store the deviation values in a new colum delta_y
        test_data["delta_y"] = test_data.iloc[:, 3:7].max(axis=1)
        return test_data

    def predict_test_values_and_store_min_deviation(self, test_data=None, poly_dict=None):
        """
        This method is used to calculate the predicted values for each training functions and take the min values among
        those regression values and store it in a new column in the 'delta_y' in the test_data dataframe
        :param test_data: test_data is the loaded csv as a dataframe
        :param poly_dict: This holds the polynomial transformer and linear regression model for each training function.
        :return: This returns the modified test_data with added columns as delta_y which stores min deviation
        """

        if test_data is None:
            raise ValueError({"message": "The test data can't be empty", "data": None})

        if poly_dict is None:
            raise ValueError({"message": "The polynomial regression models and transformers are empty", "data": None})
        # predicting the test values
        x_val = test_data['x']
        y_val = test_data['y']

        # For each x,y test pair, the value for the feature x can be predicted using 4 different training models.
        # The predicted values will be evaluated to calculate the deviation and then check for the condition.
        # to find out the mapped ideal function
        for idx, pol in poly_dict.items():
            # transform the x value using the transformer
            x_trans_val = pol["transformer"].fit_transform(x_val.values.reshape(len(test_data), 1))

            # predict the y val using the poly model for the given x value.
            y_pred_val = pol["model"].predict(x_trans_val)

            # converting the values to series from nd array
            y_pred_val_series = y_pred_val.reshape(len(y_pred_val), )

            # Calculating the delta values
            # The delta is calculated in such a way that it aligns with others deviations so, we consider -
            # - deviation squared.
            test_data[idx] = (y_pred_val_series - y_val) ** 2

        # print(test_data.head())
        # store the deviation values in a new colum delta_y
        test_data["delta_y"] = test_data.iloc[:, 3:7].min(axis=1)
        return test_data

    def map_ideal_function_to_test_data(self, test_data:None, mapping_dict=None):
        """
        This maps the ideal function to the x,y pair based on the condition max regression deviation should not exceed
        the largest deviation between train and its ideal mapping functions by a factor of sqrt(2)
        :param test_data: This is the test_data dataframe having the delta_y information which will be used to calculate
        the conditions
        :param mapping_dict: This mapping dictionary has the mapped ideal function to the train function along with the
        largest deviation among them multiplied by a factor of sqrt(2)
        :return: This will return the mapped ideal functions as per the condition in the new colum *num_ideal*
        """

        if test_data is None:
            raise ValueError({"message": "The test data can't be empty", "data": None})

        if mapping_dict is None:
            raise ValueError({"message": "The mapping between training and ideal functions are empty", "data": None})

        # setting a new colum 'num_ideal' for the test_data and assigning the column to empty text
        test_data["num_ideal"] = ""

        # Iterate through the test x,y pair one by one to find the mapped ideal function
        num_ideal_fun_list = []
        for t_data in range(len(test_data)):
            # Index(['x', 'y', 'num_cols', 'y1', 'y2', 'y3', 'y4', 'delta_y'], dtype='object')
            num_ideal_val = ""
            for idx, mapping in mapping_dict.items():
                # This is the largest deviation value calculated between training function and its chosen ideal function
                # The factor sqrt(2) is multiplied while evaluating this value
                largest_dev = mapping["largestDeviation"]

                # This is the mapped ideal function of a given training function
                mapped_ideal_fun = mapping["ideal"]
                max_dev_val = test_data.loc[t_data]["delta_y"]

                # max regression dev should not exceed the max deviation between train fun and its chosen ideal fun by -
                # - a factor of sqrt(2)
                if max_dev_val < largest_dev:
                    # adding up the matched ideal functions
                    num_ideal_val = num_ideal_val + mapped_ideal_fun + " ,"
            num_ideal_fun_list.append(num_ideal_val)

        # attaching the evaluated ideal functions to the original test_data in a column num_ideal
        test_data["num_ideal"] = num_ideal_fun_list
        return test_data
