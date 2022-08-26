from pandas import read_csv
import os
from task.db import Database
from task.exceptions.errors import ObjectNoneError
from task.model.ideal import Ideal
from task.model.test import Test
from task.model.train import Train


class LoadData:

    def __init__(self, connection=None):
        if connection is None:
            db = Database()
            self.conn = db.get_database_connection()
        else:
            self.conn = connection

    @staticmethod
    def load_train_data(file_path=None):
        """
        file_path is the relative path from the main.py file and if it is not provided,
        the files in the resource folder would be considered.
        This is to load the Training Data
        :param file_path: file path is the relative file path to the main.py file
        :return: Loaded Dataframe from CSV
        """
        try:
            path = "resources/train.csv"
            if file_path is not None:
                path = file_path
            current_dir = os.path.curdir
            train_file_path = os.path.join(current_dir, path)
            return read_csv(train_file_path)
        except FileNotFoundError:
            print("{} is not found to load the training data".format(train_file_path))
            return

    @staticmethod
    def load_ideal_data(file_path=None):
        """
        file_path is the relative path from the main.py file and if it is not provided,
        the files in the resource folder would be considered.
        This is to load the Ideal Data
        :param file_path: file path is the relative filepath to the main.py file
        :return: Loaded dataframe from CSV
        """
        try:
            path = "resources/ideal.csv"
            if file_path is not None:
                path = file_path
            current_dir = os.path.curdir
            train_file_path = os.path.join(current_dir, path)
            return read_csv(train_file_path)
        except FileNotFoundError:
            print("{} is not found to load the training data".format(train_file_path))
            return

    @staticmethod
    def load_test_data(file_path=None):
        """
        file_path is the relative path from the main.py file and if it is not provided,
        the files in the resource folder would be considered.
        This is to load the Test Data
        :param file_path: Relative file path from the main.py has to be supplied if not file in the resources folder will
        be considered
        :return: Loaded dataframe from csv
        """
        try:
            path = "resources/test.csv"
            if file_path is not None:
                path = file_path
            current_dir = os.path.curdir
            train_file_path = os.path.join(current_dir, path)
            return read_csv(train_file_path)
        except FileNotFoundError:
            print("{} is not found to load the training data".format(train_file_path))
            return

    def add_train_data_to_database(self, file_path=None, train_obj: Train = None):
        """
        This method loads the train data from the dataset and then loads into the database
        :param file_path: relative file path
        :param train_obj:
        :return: training data
        """
        if train_obj is None:
            print("The train object should not be None for the values to be created")
            raise ObjectNoneError({"message": "The train object is None"})
        # Creating an empty list
        value_list = list()

        # pick the data from the csv
        train_data = self.load_train_data(file_path=file_path)
        row_count = len(train_data)
        for i in range(0, row_count):
            value_dict = dict()
            value_dict['id'] = i + 1
            columns_list = train_data.columns
            for j in columns_list:
                value_dict[j] = train_data.loc[i][j]
            value_list.append(value_dict)
        # The value list is generated, now it has to be inserted to the database
        train_obj.insert_data_list(value_list=value_list)
        return train_data

    def add_ideal_data_to_database(self, file_path=None, ideal_obj: Ideal = None):
        """
        This method loads the ideal data from the dataset and then loads into the database
        :param file_path: relative file path from main.py if not file in the resource folder will be considered
        :param ideal_obj:
        :return: ideal dataframe
        """
        if ideal_obj is None:
            print("The train object should not be None for the values to be created")
            return
        # Creating an empty list
        value_list = list()

        # pick the data from the csv
        ideal_data = self.load_ideal_data(file_path=file_path)
        row_count = len(ideal_data)
        for i in range(0, row_count):
            value_dict = dict()
            value_dict['id'] = i + 1
            columns_list = ideal_data.columns
            for j in columns_list:
                value_dict[j] = ideal_data.loc[i][j]
            value_list.append(value_dict)
        # The value list is generated, now it has to be inserted to the database
        ideal_obj.insert_data_list(value_list=value_list)
        return ideal_data

    def add_test_data_to_database(self, test_obj: Test = None, test_data=None):

        """
        This method executes the test data line by line and will add to the database.
        :param test_obj: This is the test object that is created by the model used to create the query.
        :param test_data: this is the test data dataframe which has the final result of how many functions mapped.
        :return: return True, if everything works fine.
        """

        if test_obj is None and test_data is None:
            print("The test object should not be None for the values to be created")
            return
        # Creating an empty list
        value_list = list()

        row_count = len(test_data)
        for i in range(0, row_count):
            value_dict = dict()
            value_dict['id'] = i + 1
            # As only these columns needs to be stored in the database in this order, only iterated on them
            columns_list = ['x', 'y', 'delta_y', 'num_ideal']
            for j in columns_list:
                value_dict[j] = test_data.loc[i][j]
            value_list.append(value_dict)
        # The value list is generated, now it has to be inserted to the database
        test_obj.insert_data_list(value_list=value_list)
        return True
