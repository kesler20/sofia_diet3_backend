import unittest
from test_base import Test_ExcelDatabase
import pandas

class Test_IO_ExcelDatabase(Test_ExcelDatabase):

    def test_io_folder_name(self):
        """
        test the folder_name method which accepts the following arguments:

        ---
        Returns:
        - str
        """
        # call the folder_name getter
        test_result = self.test_client.folder_name

        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), str)

    def test_io_database(self):
        """
        test the database method which accepts the following arguments:

        ---
        Returns:
        - DataFrame
        """

        test_result = self.test_client.database

        self.assertEqual(type(test_result), pandas.DataFrame)

    def test_io_database_info(self):
        """
        test the database_info method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        test_result = self.test_client.database_info
        self.assertEqual(type(test_result), type(None))

    def test_io_create_table(self):
        """
        test the create_table method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method being tested
        correct_input = ["test_table", ["test_col1", "test_col2", "test_col3"], [
            [0, 1, 2], [2, 3, 4], [2, 3, 4]]]

        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [0, ["test_col1", "test_col2", "test_col3"], [
            [0, 1, 2], [2, 3, 4], [2, 3, 4]]]

        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = ["test_table", ["test_col1", "test_col2", "test_col3"], [
            [0, 1, 2], [2, 3, 4], [2, 3]]]

        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.create_table(*correct_input)
        self.assertEqual(test_result, correct_output[0])

        test_result = self.test_client.create_table(*invalid_types_input)
        self.assertEqual(test_result, invalid_types_output[0])

        test_result = self.test_client.create_table(*invalid_values_input)
        self.assertEqual(test_result, invalid_values_output[0])

    def test_io_get_table(self):
        """
        test the get_table method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - DataFrame
        """
        # array of arguments which are expected by the method being tested
        correct_input = ["test_table"]
        # array containing the expected correct result of the function call
        correct_output = [pandas.DataFrame([])]
        # array of arguments containing an invalid type
        invalid_types_input = [0]
        # array containing the result of the function call
        invalid_types_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid value
        invalid_values_input = [""]
        # array containing the result of the function call
        invalid_values_output = [pandas.DataFrame([])]

        test_result = self.test_client.get_table(*correct_input)
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_table(*invalid_types_input)
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_table(*invalid_values_input)
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_query_table(self):
        """
        test the query_table method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - DataFrame
        """
        # array of arguments which are expected by the method being tested
        correct_input = [lambda item: item["test_col1"] >= 1, "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid type
        invalid_types_input = [lambda item: item["test_col1"] >= 1, 0]
        # array containing the result of the function call
        invalid_types_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid value
        invalid_values_input = [lambda item: item["test_col1"] >= 1, ""]
        # array containing the result of the function call
        invalid_values_output = [pandas.DataFrame([])]

        test_result = self.test_client.query_table(*correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.query_table(*invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.query_table(*invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_get_table_slice(self):
        """
        test the get_table_slice method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [["test_col1"], "test_table", (0, 1)]
        # array containing the expected correct result of the function call
        correct_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid type
        invalid_types_input = [[0], "test_table", (0, 1)]
        # array containing the result of the function call
        invalid_types_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid value
        invalid_values_input = [[], "test_table", None]
        # array containing the result of the function call
        invalid_values_output = [pandas.DataFrame([])]

        test_result = self.test_client.get_table_slice(*correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_table_slice(*invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_table_slice(*invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_get_n_rows_from_tables_above(self):
        """
        test the get_n_rows_from_tables_above method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [5, "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid type
        invalid_types_input = ["", "test_table"]
        # array containing the result of the function call
        invalid_types_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid value
        invalid_values_input = [0, ""]
        # array containing the result of the function call
        invalid_values_output = [pandas.DataFrame([])]

        test_result = self.test_client.get_n_rows_from_tables_above(
            *correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_n_rows_from_tables_above(
            *invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_n_rows_from_tables_above(
            *invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_get_n_rows_from_tables_below(self):
        """
        test the get_n_rows_from_tables_below method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [5, "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid type
        invalid_types_input = ["", "test_table"]
        # array containing the result of the function call
        invalid_types_output = [pandas.DataFrame([])]

        # array of arguments containing an invalid value
        invalid_values_input = [0, ""]
        # array containing the result of the function call
        invalid_values_output = [pandas.DataFrame([])]

        test_result = self.test_client.get_n_rows_from_tables_below(
            *correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_n_rows_from_tables_below(
            *invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_n_rows_from_tables_below(
            *invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_table_info(self):
        """
        test the table_info method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = ["test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [0]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = [""]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.table_info(*correct_input)
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.table_info(*invalid_types_input)
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.table_info(*invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_get_table_names(self):
        """
        test the get_table_names method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - List[str]
        """
        test_result = self.test_client.get_table_names()
        self.assertEqual(type(test_result), type([]))

    def test_io_get_value_by_column_name(self):
        """
        test the get_value_by_column_name method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [0, "test_col1", "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [0]

        # array of arguments containing an invalid type
        invalid_types_input = [0, 0, "test_table"]
        # array containing the result of the function call
        invalid_types_output = [0]

        # array of arguments containing an invalid value
        invalid_values_input = [0, "", "test_table"]
        # array containing the result of the function call
        invalid_values_output = [0]

        test_result = self.test_client.get_value_by_column_name(*correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_value_by_column_name(
            *invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_value_by_column_name(
            *invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_get_value_by_column_index(self):
        """
        test the get_value_by_column_index method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [0, 0, "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [0]

        # array of arguments containing an invalid type
        invalid_types_input = [0, "test_col1", "test_table"]
        # array containing the result of the function call
        invalid_types_output = [0]

        # array of arguments containing an invalid value
        invalid_values_input = [0, "", "test_table"]
        # array containing the result of the function call
        invalid_values_output = [0]

        test_result = self.test_client.get_value_by_column_index(
            *correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.get_value_by_column_index(
            *invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.get_value_by_column_index(
            *invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_delete_table(self):
        """
        test the delete_table method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = ["test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [0]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = [""]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.delete_table(*correct_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.delete_table(*invalid_types_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.delete_table(*invalid_values_input)
        # assert that the type returned by the method is correct
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_append_row(self):
        """
        test the append_row method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method being tested
        correct_input = [[0], "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [[""], "test_table"]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = [0, "test_table"]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.append_row(*correct_input)
        self.assertEqual(test_result, correct_output[0])

        test_result = self.test_client.append_row(*invalid_types_input)
        self.assertEqual(test_result, invalid_types_output[0])

        test_result = self.test_client.append_row(*invalid_values_input)
        self.assertEqual(test_result, invalid_values_output[0])

    def test_io_delete_rows(self):
        """
        test the delete_rows method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method being tested
        correct_input = [[0], "test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [[0], ""]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = [[0], 0]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.delete_rows(*correct_input)
        self.assertEqual(type(test_result), type(correct_output[0]))

        test_result = self.test_client.delete_rows(*invalid_types_input)
        self.assertEqual(type(test_result), type(invalid_types_output[0]))

        test_result = self.test_client.delete_rows(*invalid_values_input)
        self.assertEqual(type(test_result), type(invalid_values_output[0]))

    def test_io_put_column(self):
        """
        test the put_column method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method being tested
        correct_input = ["test col",[1,2,3],"test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [0,[1,2,3],"test_table"]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = ["",[1,2,3],"test_table"]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.put_column(*correct_input)
        self.assertEqual(test_result, correct_output[0])

        test_result = self.test_client.put_column(*invalid_types_input)
        self.assertEqual(test_result, invalid_types_output[0])

        test_result = self.test_client.put_column(*invalid_values_input)
        self.assertEqual(test_result, invalid_values_output[0])

    def test_io_insert_column(self):
        """
        test the insert_column method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method being tested
        correct_input = [0,"test_col2",[0,1,2],"test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = ["","test_col2",[0,1,2],"test_table"]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = [0,"",[0,1,2],"test_table"]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.insert_column(*correct_input)
        self.assertEqual(test_result, correct_output[0])

        test_result = self.test_client.insert_column(*invalid_types_input)
        self.assertEqual(test_result, invalid_types_output[0])

        test_result = self.test_client.insert_column(*invalid_values_input)
        self.assertEqual(test_result, invalid_values_output[0])

    def test_io_delete_columns(self):
        """
        test the delete_columns method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method being tested
        correct_input = [["test_col1"],"test_table"]
        # array containing the expected correct result of the function call
        correct_output = [None]

        # array of arguments containing an invalid type
        invalid_types_input = [[""],"test_table"]
        # array containing the result of the function call
        invalid_types_output = [None]

        # array of arguments containing an invalid value
        invalid_values_input = ["","test_table"]
        # array containing the result of the function call
        invalid_values_output = [None]

        test_result = self.test_client.delete_columns(*correct_input)
        self.assertEqual(test_result, correct_output[0])

        test_result = self.test_client.delete_columns(*invalid_types_input)
        self.assertEqual(test_result, invalid_types_output[0])

        test_result = self.test_client.delete_columns(*invalid_values_input)
        self.assertEqual(test_result, invalid_values_output[0])

if __name__ == "__main__":
    unittest.main()
