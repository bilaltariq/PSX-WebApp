import sqlite3
import pandas as pd

"""
This class performs DML and DDL task for sqlite3.
"""


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    """
    Connect to the SQLite database. If it does not exist, it will be created.
    Exception will made if Connection failed.
    """

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(f"Error: Unable to connect to SQLite database. {e}")

    """
    Close connection after performing DB Operations.
    """

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    """
    Input: table_name: Table name
    Columns_dict: Dictionary where keys are column name and values are datatype (sqlite compatible)
    """

    def create_table(self, table_name, columns_dict):
        try:
            # Use a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Construct the CREATE TABLE query
            columns_str = ', '.join([f"{col_name} {col_desc}" for col_name, col_desc in columns_dict.items()])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"

            # Execute the query
            cursor.execute(create_table_query)
            print(f"Table {table_name} created (if not exists).")

            self.connection.commit()
            cursor.close()

        except sqlite3.Error as e:
            print(f"Error: Unable to create table {table_name}. {e}")

    """
    Input: table_name: Table Name
    dataframe: Data table to be inserted.
    if_exists_m = We can either replace or append. By default it is set to replace. 
    Insert data in Database.
    """

    def insert_dataframe(self, table_name, dataframe, if_exists_m='replace'):
        try:
            # Use the to_sql method to insert the DataFrame into the database
            dataframe.to_sql(table_name, self.connection, if_exists=if_exists_m, index=False)
            print(f"Data inserted into table {table_name}. Number of rows inserted: {len(dataframe)} \n")

            # Commit the changes
            self.connection.commit()

        except sqlite3.Error as e:
            print(dataframe.dtypes)
            print(dataframe)
            print(f"Error: Unable to insert data into table {table_name}. {e}")
            exit(-1)

    """
    Select all rows and columns for a table in DB.
    """

    def select_table(self, table_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result_df = pd.DataFrame(rows, columns=columns)
            cursor.close()
            return result_df

        except sqlite3.Error as e:
            print(f"Error: Unable to execute SELECT query on table {table_name}. {e}")
            return None

    """
    This method creates a dictionary for creating DDL. 
    Dict has keys as column name and values are data type (sqlite3 compatible)
    """

    def df_to_sqlite_dict(self, df):
        sqlite_data_types = {
            'int64': 'INTEGER',
            'float64': 'NUMERIC',
            'object': 'TEXT',
            'datetime64[ns]': 'TEXT'
        }

        columns_dict = {}
        for column, dtype in df.dtypes.items():
            sqlite_type = sqlite_data_types.get(str(dtype), 'TEXT')
            columns_dict[column] = sqlite_type

        return columns_dict

