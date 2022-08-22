from sqlalchemy import Column, Integer, Float, MetaData, Table
from task.db import Database
import sqlalchemy as sql

"""
This is the Ideal dataset model to store the ideal values from the Ideal.csv
"""


class Ideal:

    def __init__(self, db=None):
        if db is None:
            db = Database(echo=False)
        # Setting the engine and connection for it to be used to create the DDL and to perform CRUD operations
        self.engine = db.get_database_engine()
        self.conn = db.get_database_connection()
        self.ideal = self.create()

    def create(self):
        """
        Table structure to create ideal table
        :return:
        """
        meta = MetaData()
        ideal = Table(
            'ideal', meta,
            Column('id', Integer, primary_key=True),
            Column('x', Float),
            Column('y1', Float),
            Column('y2', Float),
            Column('y3', Float),
            Column('y4', Float),
            Column('y5', Float),
            Column('y6', Float),
            Column('y7', Float),
            Column('y8', Float),
            Column('y9', Float),
            Column('y10', Float),
            Column('y11', Float),
            Column('y12', Float),
            Column('y13', Float),
            Column('y14', Float),
            Column('y15', Float),
            Column('y16', Float),
            Column('y17', Float),
            Column('y18', Float),
            Column('y19', Float),
            Column('y20', Float),
            Column('y21', Float),
            Column('y22', Float),
            Column('y23', Float),
            Column('y24', Float),
            Column('y25', Float),
            Column('y26', Float),
            Column('y27', Float),
            Column('y28', Float),
            Column('y29', Float),
            Column('y30', Float),
            Column('y31', Float),
            Column('y32', Float),
            Column('y33', Float),
            Column('y34', Float),
            Column('y35', Float),
            Column('y36', Float),
            Column('y37', Float),
            Column('y38', Float),
            Column('y39', Float),
            Column('y40', Float),
            Column('y41', Float),
            Column('y42', Float),
            Column('y43', Float),
            Column('y44', Float),
            Column('y45', Float),
            Column('y46', Float),
            Column('y47', Float),
            Column('y48', Float),
            Column('y49', Float),
            Column('y50', Float),
        )
        meta.create_all(self.engine)
        return ideal

    def insert_data_list(self, value_list=None):
        """
        Inserting the data as list of Objects
        :param value_list: list of the objects that are to be inserted to the database table
        :return:
        """
        if value_list is not None:
            query = sql.insert(self.ideal)
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
        Fetch all records, which is like select query to verify all the records of the ideal table
        :return:
        """
        try:
            query = sql.select(self.ideal)
            result_proxy = self.conn.execute(query)
        except Exception as ex:
            error = str(ex.__dict__)
            print(error)
        else:
            print("The records are: ", result_proxy.fetchall())