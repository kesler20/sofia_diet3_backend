import pandas as pd
import os
from table_schema import SQL_STATEMENTS
from datetime import datetime
from typing import Dict, Optional, List, Any, Tuple, Union
try:
    from database_client import DatabaseClient
except ModuleNotFoundError:
    from src.protocol_backend.protocol_database.database_client import DatabaseClient

'''The database interface should allow you to implement different database clients from a single Object
The notes for the SQL queries can be found here 
https://github.com/kesler20/Config_settings/blob/master/mySQL/notes.md

The notes for the sqlite3 documentation in python can be found here 
https://docs.python.org/3/library/sqlite3.html#cursor-objects
'''


SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M.%S'
SESSION_ID = datetime.now().strftime(SQL_DATETIME_FORMAT)


class DatabaseInterface(object):
    '''The database interface is used to perform CRUD operations on various form of databases i.e. SQL 

    Properties
    ---
      client - the client is an SQLClient object yielded by the context manager
    this can be initialized as follows

    ```python
    client = DatabaseClient("my_database_path.db")
    db = DatabaseInterface(db)
    ```

    The Database Interface supports CRUD operations on tables with the following format:

    ```python
    sql_statements = ["""
    CREATE TABLE parent (
        id integer primary key autoincrement,
        name varchar(255)
    );
    """,
    """
    CREATE TABLE child (
        id integer primary key autoincrement,
        name varchar(255),
        parent_id integer not null,
        foreign key (parent_id) references parent(id) 
    );
    """
    ]
    for statement in sql_statement:
        print(db.run_query("*"))
    ```

    the type of data to insert is
    | id  | name        | foreign key |
    | --- | ----------- | ----------- |
    | 1   | test_data n | 1           |
    '''

    def __init__(self, client: DatabaseClient) -> None:
        self.client = client

    def run_query(self, query: str, key: str) -> List[Any]:
        """Run a query on the selected database

        Params
        ---
        query: str 
          the query that will be performed to the database

        key: str 
          the key that will be used to retrieve the values within the query
          if the key is left as "" this will be ignored 
          if the key is set at "*" all the keys will be returned

        Returns
        ---
        result: list 
          list of values"""

        result = []
        with self.client as client:
            print(query)
            query_values: List[Dict[str, Any]] = client.cursor.execute(query)
            client.connection.commit() 

            if key == "":
                pass
            elif key == "*":
                for value in query_values:
                    result.append(tuple([value[key] for key in value.keys()]))
            else:
                for value in query_values:
                    result.append(value[key])

        if result == []:
            print(result)

        return result

    def create_tables(self, table_name: str, columns: Dict[str, Any], foreign_key: Optional[str] = None) -> None:
        '''Creates a table

        Params
        ---
        table_name: str 
          name iof the table to create

        columns : dict
          this is the DietBase.columns output a dictionary of the following
          form { 'column_name' : <class 'str'> }

        foreign_key : None or str
          this will set the parentId to the given Key,
          to remove the parentId set this parameter as None

        Example
        ---
        example on how to use it with an example of a Food object
        ```python
        db.create_tables("Food", fd.columns, "Session")
        ```

        this will generate the following output:
        ```sql
        CREATE TABLE Food(id INTEGER PRIMARY KEY AUTOINCREMENT,
            protein INTEGER NOT NULL,
            calories INTEGER NOT NULL,
            cost FLOAT NOT NULL,
            amount FLOAT NOT NULL,
            name VARCHAR(255) NOT NULL,
            total VARCHAR(255) NOT NULL,
            vendorname VARCHAR(255) NOT NULL,
            receiptname VARCHAR(255) NOT NULL,
            FOREIGN KEY(id) REFERENCES Session(id)
        );
        ```
        '''
        # trying to generate a string like the ones listed in the table_schema.py file
        # initialise the body of the create table statement
        # within the system is assumed that each row of the table is identified
        # by the autoincrement id variable which is an integer
        create_statement_body = '''id INTEGER PRIMARY KEY AUTOINCREMENT,'''
        for column_name in columns.keys():
            raw_column_type = columns[column_name]
            # convert the types of each column using the internal function
            converted_column_type = self.convert_to_sql_type(raw_column_type)
            # if the column_name is not the last one in the array
            if not column_name == list(columns.keys())[-1]:
                create_statement_body += '''
    {} {} NOT NULL,'''.format(column_name, converted_column_type)
            else:
                # if you reach the last item check whether a foreign key is provided or not
                if foreign_key is None:
                    create_statement_body += '''
    {} {} NOT NULL,
    FOREIGN KEY(id) REFERENCES {}(id)  
);'''.format(column_name, converted_column_type, foreign_key)
                else:
                    create_statement_body += '''
    {} {} NOT NULL    
);'''.format(column_name, converted_column_type)

        create_table_sql_statement = '''CREATE TABLE {}('''.format(table_name)
        create_table_sql_statement += create_statement_body

        with self.client as client:
            client.cursor.execute(create_table_sql_statement)
            print(create_table_sql_statement)
            client.connection.commit()

    def convert_to_sql_type(self, python_type) -> str:
        if python_type == int:
            return "INTEGER"
        elif python_type == float:
            return "FLOAT"
        elif python_type == str:
            return "VARCHAR(255)"
        elif python_type == datetime:
            return "DATETIME"
        else:
            return "VARCHAR(255)"

    def update_tables(self, sql_statement: str) -> None:
        '''Update tables 

        params:
        * sql_statement - str, an sql statement that will be run on an existing table
        '''
        with self.client as client:
            client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()

    def delete_tables(self, table_name: str) -> None:
        '''Deletes the selected table from the database

        params:
        * table_name - str, name of the table to delete from the database'''

        sql_statement = '''DROP TABLE {}'''.format(table_name)
        with self.client as client:
            client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()

    def create_values(self, columns: str, values: Union[Tuple[Optional[str],float], str], table_name: str) -> None:
        '''Create the values

        params:
        * columns - tuple, a tuple containing the columns you want to insert into
        * values - tuples, tuples representing tuples of values that you want to insert into the table
        * table_name - str, the name of the table which we want to modify

        for instance
        ```python
        db.create_values("(session_id)", """("value to insert")""", "Session")
        ```
        this is because the string that will call the insert statement 
        requires the double quotes symbol as such "value"
        '''

        sql_statement = f'''INSERT INTO {table_name} {columns} VALUES {values}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def read_all_values_from_table(self, table_name: str) -> List[Tuple[Any,...]]:
        '''Describe method'''

        result = []
        sql_statement = f'''SELECT * FROM {table_name}'''
        with self.client as client:
            values: List[Dict[str, Any]] = client.cursor.execute(sql_statement)
            client.connection.commit()
            for value in values:
                result.append(tuple([value[col]
                              for col in list(value.keys())]))

        return result

    def read_all_values_from_column(self, column_name: str, table_name: str) -> List[Any]:
        '''Read all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of

        returns:
        * values - list, a list of tuples of values'''

        result = []
        sql_statement = f'''SELECT {column_name} FROM {table_name}'''
        with self.client as client:
            values = client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()
            for value in values:
                result.append(value[column_name])

        print(result)
        return result

    def read_value(self, column_name: str, table_name: str, primary_key: int, parent_id: int) -> List[Any]:
        '''Read all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of
        * primary_key - int, the primary key of the value that we want to retrieve
        * parent_id - the name of the foreign key which references to the parent table

        returns:
        * values - list, a list of tuples of values'''

        result = []
        sql_statement = f'''SELECT {column_name} FROM {table_name} WHERE {parent_id} = {primary_key}'''
        with self.client as client:
            values = client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()
            for value in values:
                result.append(value[column_name])
        print(result)
        return result

    def update_value(self, column_name: str, table_name: str, primary_key: int, value: str, parent_id: int) -> None:
        '''Update a value within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of
        * primary_key - int, the primary key of the value that we want to retrieve
        * parent_id - the name of the foreign key which references to the parent table
        '''

        sql_statement = f'''UPDATE {table_name} SET {column_name} = "{value}" WHERE {parent_id} = {primary_key}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def delete_value(self, table_name: str, parent_id_value: int, parent_id_key: str) -> None:
        '''Delete a value from the table

        param:
        * table_name - str, the name of the table we want to read the values of
        * parent_id_value - int, the primary key of the value that we want to retrieve
        * parent_id_key - the name of the foreign key which references to the parent table
        '''

        sql_statement = f'''DELETE FROM {table_name} WHERE {parent_id_key} = {parent_id_value}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def delete_all_values(self, table_name: str) -> None:
        '''Delete all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        '''

        delete_statement = f'''DELETE FROM {table_name}'''
        with self.client as client:
            print(delete_statement)
            client.cursor.execute(delete_statement)
            client.connection.commit()

    def convert_sql_table_to_df(self, column_names: 'list[str]', table_name: str):
        named_rows = [list(zip(column_names, row))
                      for row in self.read_all_values_from_table(table_name)]
        print(self.read_all_values_from_table(table_name))

        data_frames: 'list[pd.DataFrame]' = []
        for row_id, row in enumerate(named_rows):
            data_array = {row[0]: [row[1]] for row in named_rows[row_id]}
            df = pd.DataFrame(data=data_array)
            data_frames.append(df)

        main_df = pd.concat(data_frames)
        main_df.set_index("id", inplace=True)
        print(f"--------------{table_name}--------------------")
        print(main_df)
        return main_df

if __name__ == "__main__":
    os.remove(r"sql_files\my_routine.db")
    client = DatabaseClient(r"sql_files\my_routine.db")
    db = DatabaseInterface(client)
    for statement in SQL_STATEMENTS:
        print(statement)
        db.run_query(statement, "")
