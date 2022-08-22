from sqlalchemy import Column, Integer, Float, MetaData, Table
from task.db import Database
import sqlalchemy as sql


"""
This is the Train dataset model to store the train values from train.csv
"""


class Train:

    def __init__(self, db=None):
        if db is None:
            db = Database(echo=False)

        # Setting the engine and connection for it to be used to create the DDL and to perform CRUD operations
        self.engine = db.get_database_engine()
        self.conn = db.get_database_connection()
        self.train = self.create()

    def create(self):
        """
        This is to create the database table
        :return: It returns the table object
        """
        meta = MetaData()
        train = Table(
            'train', meta,
            Column('id', Integer, primary_key=True),
            Column('x', Float),
            Column('y1', Float),
            Column('y2', Float),
            Column('y3', Float),
            Column('y4', Float),
        )
        meta.create_all(self.engine)
        return train

    def insert_data_list(self, value_list=None):
        """
        Inserting the data as list of Objects
        :param value_list: List of objects which are to be inserted into the Database
        :return:
        """
        if value_list is not None:
            query = sql.insert(self.train)
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

    def fetch_all_records(self):
        """
        Fetch all records, which is like select query to verify all the records of the train table
        :return:
        """
        try:
            query = sql.select(self.train)
            result_proxy = self.conn.execute(query)
        except Exception as ex:
            error = str(ex.__dict__)
            print(error)
        else:
            print("The records are: ", result_proxy.fetchall())
