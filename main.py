import math

from task.db import Database
from task.model.test import Test
from task.model.train import Train
from task.model.ideal import Ideal
from task.loaddata import LoadData
from task.idealmapping import IdealMapping
from task.polytrain import PolyTrain
from task.testmapping import TestMapping

"""
This is the main method where the execution starts
"""
if __name__ == '__main__':

    # Creating a SQLite database connection and name it as test.db
    # The default logging can be managed using the echo parameter, to turn off logging use echo as False
    db = Database(echo=True)

    # Creating the Train Table
    # The db object is passed to reduce the number of connections
    train = Train(db=db)
    train.create()

    # Creating the Ideal Table
    # The db object is passed to reduce the number of connections
    ideal = Ideal(db=db)
    ideal.create()

    # Listing the tables in the connection
    # print(db.engine.table_names())

    # Load train data and insert it into the database,
    # we should pass the connection to make sure the engine is not getting created again
    load_data = LoadData(connection=db.get_database_connection())
    train_data = load_data.add_train_data_to_database(train_obj=train)
    train_columns = train_data.columns

    # Enable the below line to query all the train records from the database
    # train.fetch_all_records()

    # Load the Ideal data and insert it to the database
    ideal_data = load_data.add_ideal_data_to_database(ideal_obj=ideal)
    ideal_columns = ideal_data.columns
    # Enable the below line to query all the train records from the database
    # ideal.fetch_all_records()

    # Map the ideal functions to the training function and store it in a dictionary
    mapping_dict = dict()
    mapping_obj = IdealMapping()
    for i in range(1, len(train_columns)):
        train_function = train_columns[i]
        (min_least_squared_value, mapped_ideal_function, largest_deviation_value, smallest_deviation_value) = \
            mapping_obj.map_ideal_function(
                df_train=train_data, df_ideal=ideal_data, train_col=train_function, plot=False)
        # Mapped ideal function is stored in a dictionary
        mapping_dict.__setitem__(train_function, {"ideal": mapped_ideal_function, "minSum": min_least_squared_value,
                                                  "largestDeviation": largest_deviation_value * math.sqrt(2),
                                                  "smallestDeviation": smallest_deviation_value})
        print("The ideal function for the function {} is {}".format(train_function, mapped_ideal_function))
        print(mapping_dict)

    # Training the (x,y) pair using Polynomial Regression
    poly_dict = dict()
    poly_obj = PolyTrain()
    for i in range(1, len(train_columns)):
        (poly_model, poly_transform) = poly_obj.polynomial_regression_df(df=train_data,
                                                                         train_function_col=train_columns[i],
                                                                         feature_col=train_columns[0],
                                                                         plot=False)
        poly_dict.__setitem__(train_columns[i], {"transformer": poly_transform, "model": poly_model})

    # Loading the test data
    test_data = load_data.load_test_data(file_path=None)

    # Loading the test mapping class
    test_mapping = TestMapping()

    # This function sets the max deviation values in the among the regression values calculated using the regression
    test_data = test_mapping.predict_test_values_and_store_max_deviation(test_data=test_data, poly_dict=poly_dict)

    # Evaluate the ideal functions that can be mapped to the test dataset
    test_data = test_mapping.map_ideal_function_to_test_data(test_data=test_data, mapping_dict=mapping_dict)

    # Initialize the test model and create the table
    test = Test(db=db)
    test.create()
    # Store the data as per the required columns in the database.
    load_data.add_test_data_to_database(test_obj=test, test_data=test_data)
