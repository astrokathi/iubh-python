from sqlalchemy import create_engine
import os


class Database:

    def __init__(self, echo=True):
        """
        This Class creates the database file and creates the engine and returns values to the models
        :param echo: If this value is set to true, then we can see the debug logs of the Database
        """
        db_path = "test.db"

        if os.path.exists(db_path):
            print("Database file already exists, so deleting it as the program generates the same set "
                  "which conflicts while inserting, later once the records exists then it should not be generated")
            os.remove(db_path)
            print("The db file removed and will be re-created by establishing a new connection, this type of concept "
                  "is strictly restricted to the portable databases, for others we need to delete all the entries "
                  "before inserting the new bulk data")
        engine = create_engine('sqlite:///test.db', echo=echo)
        self.engine = engine
        try:
            self.conn = self.engine.connect()
        except Exception as e:
            error = str(e.__dict__)
            print(error)
        else:
            print("Connection established successfully")

    def get_database_engine(self):
        """
        This method is used to export the engine to the required classes/ models.
        :return: Engine of the database, to establish or create connection
        """
        return self.engine

    def get_database_connection(self):
        """
        This method is used to export the database connection to the classes/ models
        :return: Database connection using which we can query the database or insert/ delete the data.
        """
        return self.conn
