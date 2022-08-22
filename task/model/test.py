from sqlalchemy import Column, Integer, Float, MetaData, Table, String
from task.db import Database
import sqlalchemy as sql


"""
This is the Test dataset model to store the train values from test.csv
"""


class Test:

    def __init__(self, db=None):
        if db is None:
            db = Database(echo=False)

        # Setting the engine and connection for it to be used to create the DDL and to perform CRUD operations
        self.engine = db.get_database_engine()
        self.conn = db.get_database_connection()
        self.test = self.create()

    def create(self):
        """
        This is to create the database table
        :return: It returns the table object
        """
        meta = MetaData()
        test = Table(
            'test', meta,
            Column('id', Integer, primary_key=True),
            Column('x', Float),
            Column('y', Float),
            Column('delta_y', Float),
            Column('num_ideal', String)
        )
        meta.create_all(self.engine)
        return test

    def insert_data_list(self, value_list=None):
        """
        Inserting the data as list of Objects
        :param value_list: List of objects which are to be inserted into the Database
        :return:
        """
        if value_list is not None:
            query = sql.insert(self.test)
            try:
                result_proxy = self.conn.execute(query, value_list)
            except Exception as ex:
                error = str(ex.__dict__)
                print("There is an exception while inserting the data to the Train table")
                print(error)
            else:
                print("The last inserted Id is: ", result_proxy.lastrowid)
        else:
            print("Nothing to insert as the Value List is Empty")

    def insert_data_row(self, x=None, y=None, delta_y=None, num_ideal=None):
        """
        This method will create a new row in the Test table based on the values provided.
        :param x: This is the x value
        :param y: This is the y value
        :param delta_y: This the deviation value between the y and the predicted y using the training model
        :param num_ideal: This is the ideal functions that are mapped as per the provided conditions.
        :return: None
        """

        query = sql.insert(self.test)
        try:
            result_proxy = self.conn.execute(query, id=id, x=x, y=y, delta_y=delta_y, num_ideal=num_ideal)
        except Exception as ex:
            error = str(ex.__dict__)
            print("There is an exception while inserting the data to the Train table")
            print(error)
        else:
            print("The last inserted Id is: ", result_proxy.lastrowid)

    def fetch_all_records(self):
        """
        Fetch all records, which is like select query to verify all the records of the test table
        :return:
        """
        try:
            query = sql.select(self.test)
            result_proxy = self.conn.execute(query)
        except Exception as ex:
            error = str(ex.__dict__)
            print(error)
        else:
            print("The records are: ", result_proxy.fetchall())
