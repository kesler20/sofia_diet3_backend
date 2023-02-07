import os
import shutil
from pathlib import Path
import pandas as pd
from typing import List, Any, Union, Dict, Optional, Tuple, Callable
from dataclasses import dataclass
try:
    from _types import DataFrame
    from _base import folder_name
except ModuleNotFoundError:
    from src.protocol_backend.protocol_database._types import DataFrame
    from src.protocol_backend.protocol_database._base import folder_name


@dataclass
class ExcelDatabase:
    """ExcelDatabase is a class"""

    __folder_name:  str = folder_name

    @property
    def folder_name(self) -> str:
        """folder_name property getter"""
        return self.__folder_name

    def set_folder_name(self, folder_name: str):
        """folder_name property setter"""
        self.__folder_name = folder_name
        return self

    @property
    def database(self) -> DataFrame:
        """Returns a data frame which contains all the excel files within the 
        database concatenated
        """
        dfs = []
        for table in os.listdir(self.folder_name):
            dfs.append(pd.read_excel(os.path.join(self.folder_name, table)))
        if len(dfs) >= 1:
            df: DataFrame = pd.concat(dfs)
        else:
            df: DataFrame = pd.DataFrame([])
        return df

    @property
    def database_info(self) -> None:
        """database_info has the following params"""
        db = self.database
        print("General Info on the Database")
        print(db.info)
        print("These are the columns")
        print(db.columns)
        print("These are the rows")
        print(db.index)
        print("This is the count")
        print(db.count)
        print("This is the database")
        print(db)

    def __guard_clause(self, args: List[Tuple[Any, Any]], function_name) -> Any:
        """Every public method should call the guard clause
        this will guard the public method being called from invalid input types

        Parameters
        ---
        args : List[Tuple[Any,Any]]
            array of arguments of the form:
        ```python
        [(topic, str), (payload, str)]
        function_name : str
            the name of the function that we want to guard
        ```

        Returns
        ---
        return result or "guarded"
        """
        if False in [type(var) == var_type for var, var_type in args]:
            print(f"{function_name} guarded 🥵", [
                  type(var) == var_type for var, var_type in args])
            print("with the following args", [arg for arg in args])
            return None
        else:
            return "guarded"

    def __pp(self, table_name: str, message: str, table: DataFrame) -> None:
        """Pretty print, a convention to display events

        Parameters
        ---

        message : str
            to be passed as parameter 4
        table_name : str
            the name of the table to be displayed
        table : DataFrame
            the table to display

        Returns
        ---
        result: None
        """
        print(f"{message}...")
        print(f"======= {table_name} ==========")
        print(table)

    def preview_table(self, table_name: str):
        """Open the table selected in excel

        Parameters
        ---
        table_name : str
            name of hte table to preview

        Returns
        ---
        None
        """
        if self.__guard_clause([(table_name, str)], "preview_table") is None or table_name == "":
            return None
        os.system(f'''start excel {os.path.join(self.folder_name,f"{table_name}.xlsx")}''')

    def create_database(self, folder_name: str) -> None:
        """Create a database with the given database name

        Parameters
        ----
        folder_name : str
            the name of the database

        Returns
        ---
        result : None
        """
        if not Path(folder_name).exists():
            os.mkdir(folder_name)

    def delete_database(self, database_name: str) -> None:
        """Delete the excel file with the given name

        Parameters
        ---
        database_name : str
            the name of the database to delete

        Returns
        ---
        result : None
        """
        if Path(database_name).exists():
            shutil.rmtree(database_name)

    def create_table(self, table_name: str, columns: List[str], rows: List[List[Any]]) -> None:
        """create_table has the following params

        Parameters
        ---
        table_name : str
            the name of the table that we want to create
        columns : List[str]
            a list of names of the columns of the new table
        rows : List[List[Any]]
            a list of lists containing the values of the rows
            the indicies of the first list will correspond to the
            column that the values of the row belong too
            each inner list should be of the same length

        Returns
        ---
        result : None
        """

        df = pd.DataFrame(data={col: rows[i] for i, col in enumerate(columns)})

        if not Path(self.folder_name).exists():
            os.mkdir(self.folder_name)

        df.to_excel(
            os.path.join(self.folder_name, f"{table_name}.xlsx"), index=False)
        self.__pp(table_name, "Creating a Table", df)
        print("")
        print("new table at", os.path.join(
            self.folder_name, f"{table_name}.xlsx"))
        print("")

    def get_table(self, table_name: str) -> DataFrame:
        """get_table has the following params

        Parameters
        ---
        table_name : str
            the name of the table which will be returned

        Returns
        ---
        result: DataFrame
        """
        if self.__guard_clause([(table_name, str)], "get_table") is None or table_name == "":
            return pd.DataFrame([])
        try:
            df: DataFrame = pd.read_excel(os.path.join(
                self.folder_name, f"{table_name}.xlsx"))
        except FileNotFoundError:
            df = pd.DataFrame([])
        return df

    def query_table(self, query: Callable[[DataFrame], Any], table_name) -> DataFrame:
        """To query the table pass a lambda expression as the query callback which takes the df
        as an argument

        Example
        ---
        this is an example of querying values greater than or equal to 2
        ```python
        # initialise the database
        db = ExcelDatabase()
        # create a random table
        db.create_table("New Table", ["data", "another data"], [
                        [1, 2, 4, 6], [2, 10, 5, 7]])
        # query the values from the data column which are greater than or qual to 2
        print(db.query_table(lambda table: table["data"] >= 2, "New Table"))
        ```

        Output
        ---
        ```txt
        ======= New Table ==========
            data  another data
        0     1             2
        1     2            10
        2     4             5
        3     6             7
            data  another data
        1     2            10
        2     4             5
        3     6             7
        ```
        """
        # function to used for th guard clause
        def foo():
            ...

        if self.__guard_clause([(query, type(foo)), (table_name, str)], "query_table") is None or table_name == "":
            return pd.DataFrame([])

        return self.get_table(table_name).loc[query(self.get_table(table_name))]

    def get_table_slice(
        self,
        columns: Union[str, List[str]],
        table_name: str,
        index: Optional[Tuple[int, int]] = None
    ) -> DataFrame:
        """Get a specific columns and rows of the table

        Note
        ---
        when index is a tuple of integers this will be turned into a slice which goes from
        index[0] -> index[1] + 1,

        Parameters
        ---
        index : Optional[Tuple[int,int]]
          the index is a tuple of indices representing where you want t get the rows from and to
          this is of the form (from, to) where from and to are integers
          if left to None this will return all the rows

        columns : List[str] or str
          this is an array of strings in the event that we want to select more than one column
          this is a string if you only want to select one column
          if the column is set to "*" all columns will be considered

        table_name : str
            the name of the table that we want to get a slice from

        Returns
        ---
        DataFrame
        """
        if type(columns) != str and type(columns) != list:
            return pd.DataFrame([])

        if type(columns) == list:
            if len(columns) == 0:
                columns = "*"
            else:
                if False in [type(val) == str for val in columns]:
                    return pd.DataFrame([])

        if table_name == "" and type(table_name) != str:
            return pd.DataFrame([])

        if type(index) != type(None) and type(index) != tuple:
            if type(index) == tuple:
                if len(index) == 0:
                    index = None
            return pd.DataFrame([])

        table = self.get_table(table_name)
        if columns == "*":
            columns = [str(col) for col in table.columns]
        if index is None:
            return table[columns]
        return table[columns].loc[index[0]:index[1]]

    def get_n_rows_from_tables_above(self, n: int, table_name: str) -> DataFrame:
        """get_n_rows_from_tables_above has the following params

        Parameters
        ---
        n : int
            the number of values that we want to get from
        table_name : str
            to be passed as parameter 3

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
            [(n, int), (table_name, str)],
            "get_n_rows_from_tables_above"
        ) is None or table_name == "":
            return pd.DataFrame([])

        return self.get_table(table_name).head(n)

    def get_n_rows_from_tables_below(self, n: int, table_name: str) -> DataFrame:
        """get_n_rows_from_tables_below has the following params

        Parameters
        ---
        n : int
            the number of values that we want to get from
        table_name : str
            to be passed as parameter 3

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
            [(n, int), (table_name, str)],
            "get_n_rows_from_tables_below"
        ) is None or table_name == "":
            return pd.DataFrame([])

        return self.get_table(table_name).tail(n)

    def table_info(self, table_name: str) -> Any:
        """table_info has the following params

        Parameters
        ---

        table_name str
            to be passed as parameter 2

        Returns
        ---
        result: Any
        """
        if self.__guard_clause([(table_name, str)], "table_info") is None or table_name == "":
            return None

        table = self.get_table(table_name)
        print("Table info")
        print(table.info)
        print("Table Shape")
        print(table.shape)
        print("Table axes.")
        print(table.axes)

    def get_table_names(self) -> List[str]:
        """get_table_names has the following params"""
        return [file.replace(".xlsx", "") for file in os.listdir(self.folder_name)]

    def get_value_by_column_name(self, row_index: int, column_name: str, table_name: str) -> Any:
        """get_value_by_column_name has the following params

        Parameters
        ---
        row_index : int
            the index of the row that we want to get the values from
        column_name : str
            the name of the column which will searched th value from
        table_name : str
            to be passed as parameter 4

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
                [(row_index, int), (column_name, str), (table_name, str)],
                "get_value_by_column_name") is None or table_name == "" or column_name == "":
            return 0
        return int(self.get_table(table_name).at[row_index, column_name])

    def get_value_by_column_index(self, row_index: int, column_index: str,  table_name: str) -> Any:
        """get_value_by_column_index has the following params

        Parameters
        ---
        row_index : int
            the index of the row that we want to get the values from
        column_name : str
            the index of the column which will searched th value from
        table_name : str
            to be passed as parameter 4

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
                [(row_index, int), (column_index, int), (table_name, str)], "get_value_by_column_index") is None:
            return 0
        return int(self.get_table(table_name).iat[row_index, column_index])

    def delete_table(self, table_name: str) -> Any:
        """delete_table has the following params

        Parameters
        ---

        table_name str
            name of the table to delete

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
            [(table_name, str)],
            "delete_table"
        ) is None or not Path(os.path.join(self.folder_name, f"{table_name}.xlsx")).exists():
            return None

        os.remove(os.path.join(self.folder_name, f"{table_name}.xlsx"))

    def append_row(self, row: List[List[Any]], table_name: str) -> None:
        """append_row has the following params

        Parameters
        ---
        row : list[list[any]]
            a collection of items containing 1 new value for the 
            last rows of each column in the data frame, therefore
            the length of the row needs to be equal to the number of columns

        table_name : str
            the name of the table where the row will be inserted
        Returns
        ---
        result: None
        """
        if table_name == "":
            return None
        table = self.get_table(table_name)

        table.loc[len(table[table.columns[0]])] = row
        table.to_excel(os.path.join(self.folder_name,
                       f"{table_name}.xlsx"), index=False)

    def delete_rows(self, rows: List[int], table_name: str) -> None:
        """delete_rows has the following params

        Note
        ---
        This will re start the index from 0

        Parameters
        ---
        rows : list[int]
            the list of rows that we want to drop
        table_name : str
            the name of the table we want to modify

        Returns
        ---
        result: None
        """
        if self.__guard_clause(
            [(rows, list), (table_name, str)],
            "delete_rows"
        ) is None or table_name == "":
            return None

        table = self.get_table(table_name)
        print("this is the initial table")
        print(table)
        print("")
        table.drop(rows, inplace=True)
        self.__pp(table_name, "Deleting rows", table)
        table.to_excel(os.path.join(self.folder_name,
                       f"{table_name}.xlsx"), index=False)

    def put_column(self, column_name: str, column_values: List[Any], table_name: str) -> None:
        """put_column has the following params

        Parameters
        ---
        column_name : str
            the name of the column where the values will be put
        column_values : list[Any]
            a collection of objects to be stored on the column name
        table_name : str
            to be passed as parameter 4

        Returns
        ---
        result: None
        """
        if self.__guard_clause(
            [(column_name, str), (column_values, list), (table_name, str)],
            "put_column"
        ) is None or column_name == "" or column_values == [] or table_name == "":
            return None

        table = self.get_table(table_name)
        if len(column_values) < len(table[table.columns[0]]):
            diff = len(table[table.columns[0]]) - len(column_values)
            for _ in range(diff):
                column_values.append(None)

        table[column_name] = column_values
        self.__pp(table_name, "Put a new column", table)
        table.to_excel(os.path.join(self.folder_name,
                       f"{table_name}.xlsx"), index=False)

    def insert_column(self, column_index: int, column_name: str, column_values: List[Any], table_name: str) -> None:
        """insert_column has the following params

        Parameters
        ---
        column_index : int
            position of the column that we want to insert
        column_name : str
            name of the column that we want to insert
        column_values : list[Any]
            values that we want to insert into the column_name
        table_name : str
            to be passed as parameter 5

        Returns
        ---
        result: None
        """
        if self.__guard_clause(
            [(column_index, int), (column_name, str),
             (column_values, list), (table_name, str)],
            "insert_column"
        ) is None or column_name == "" or column_values == [] or table_name == "":
            return None

        table = self.get_table(table_name)
        if len(column_values) < len(table[table.columns[0]]):
            diff = len(table[table.columns[0]]) - len(column_values)
            for _ in range(diff):
                column_values.append(None)

        table.insert(column_index, column_name, column_values)
        self.__pp(table_name, "Appending a new column", table)
        table.to_excel(os.path.join(self.folder_name,
                       f"{table_name}.xlsx"), index=False)

    def delete_columns(self, columns: List[str], table_name: str) -> Any:
        """delete_columns has the following params

        Parameters
        ---
        columns : list[str]
            the list of columns that you want to pop
        table_name str
            the name of the table that you want to edit

        Returns
        ---
        result: Any
        """
        if self.__guard_clause(
            [(columns, list), (table_name, str)],
            "delete_columns"
        ) is None or table_name == "" or columns == [""]:
            return None

        table = self.get_table(table_name)
        for column in columns:
            table.pop(column)
        self.__pp(table_name, "Deleting Columns", table)
        table.to_excel(os.path.join(self.folder_name,
                       f"{table_name}.xlsx"), index=False)
