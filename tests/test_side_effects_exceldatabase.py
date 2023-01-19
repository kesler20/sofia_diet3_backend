import os
from pathlib import Path
import unittest
from test_base import (
    Test_ExcelDatabase,
    folder_name, 
    base_df, 
    base_df_cols, 
    base_df_values, 
    base_table_name,
    another_df_cols, 
    another_df_values, 
    another_df,
    another_table_name
)
import pandas as pd


class Test_SideEffects_ExcelDatabase(Test_ExcelDatabase):

    def test_side_effects_folder_name(self):
        """
        test that the getter and setter for the folder name work
        """

        # testing that the initial folder_name returned correspond to the one
        # initialized at the base
        base_output = [folder_name]
        test_result = self.test_client.folder_name
        self.assertEqual(test_result, base_output[0])

        # test that after setting a new value this is updated within the class
        side_effect_output = ["new_test_database"]
        self.test_client.set_folder_name("new_test_database")
        test_result = self.test_client.folder_name
        self.assertEqual(test_result, side_effect_output[0])

    def test_side_effects_database(self):
        """
        test that the database getter returns the correct value
        """

        # array containing the expected correct result of the side effect
        base_effect_output = [base_df]
        test_result = self.test_client.database
        self.assertTrue(test_result.equals(base_effect_output[0]))

        # cause a side effect to test
        # this side effect should be cleaned up at tear down
        # as the new table should be part of the base_database
        self.test_client.create_table(
            another_table_name, another_df_cols, another_df_values)
        side_effect_output = [pd.concat([another_df, base_df])]

        # test that the side effect is expected
        test_result = self.test_client.database
        self.assertTrue(test_result.equals(side_effect_output[0]))

    def test_side_effects_create_table(self):
        """test that a table is successfully created in path 
        """
        # test that after the folder name is created this can be found on the root dir
        self.test_client.create_table("new_test_table", ["col"], [0, 1])
        self.assertTrue(
            Path(os.path.join(folder_name, "new_test_table.xlsx")).exists())

    def test_side_effects_create_database(self):
        """test that the create_database method creates a database in path
        """
        self.test_client.create_database("new_test_db")
        self.assertTrue(Path("new_test_db").exists())

        # clean up the side effects made
        self.test_client.delete_database("new_test_db")

    def test_side_effects_get_table(self):
        """testing that a table can be retrieved from the database
        """
        # cause side effects
        # to support the test which only checks if a table is created
        # this test will also check if the create_table method creates a table with he desired values
        # cause a side effect to test
        self.test_client.create_table(
            another_table_name, another_df_cols, another_df_values)
        test_result = self.test_client.get_table(another_table_name)

        self.assertTrue(test_result.equals(another_df))

    def test_side_effects_query_table(self):
        """
        test the query_table method which accepts the following arguments:
        """
        # cause the side effect
        self.test_client.create_table(
            another_table_name, another_df_cols, another_df_values)
        # run the query
        test_result = self.test_client.query_table(
            lambda table: table[another_df_cols[0]] > another_df_values[0], another_table_name)
        # check that the result of the query matches the expected
        expected_output = pd.DataFrame(
            another_df_values, columns=another_df_cols)
        expected_output.drop([0], inplace=True)
        self.assertTrue(test_result.equals(expected_output))

    def test_side_effects_get_table_slice(self):
        """test that the correct slice of a table can be retrieved
        """

        test_result = self.test_client.get_table_slice(base_df_cols,base_table_name,(0,2))
        expected_output = pd.DataFrame(base_df_values[0:3],columns=base_df_cols)
        self.assertTrue(test_result.equals(expected_output))

    def test_side_effects_get_n_rows_from_tables_above(self):
        """
        test the get_n_rows_from_tables_above method which accepts the following arguments
        """
        # run the query
        test_result = self.test_client.get_n_rows_from_tables_above(2, base_table_name)
        # check that the result of the query matches the expected
        expected_output = pd.DataFrame(
            base_df_values, columns=base_df_cols).head(2)
        self.assertTrue(test_result.equals(expected_output))

    def test_side_effects_get_n_rows_from_tables_below(self):
        """
        test the get_n_rows_from_tables_below method which accepts the following arguments
        """
        # run the query
        test_result = self.test_client.get_n_rows_from_tables_below(2, base_table_name)
        # check that the result of the query matches the expected
        expected_output = pd.DataFrame(
            base_df_values, columns=base_df_cols).tail(2)
        self.assertTrue(test_result.equals(expected_output))

    def test_side_effects_get_table_names(self):
        """
        test the get_table_names method which accepts the following arguments
        """
        # the list of names return should correspond to the default values
        self.assertEqual(self.test_client.get_table_names(),[base_table_name])

    def test_side_effects_get_value_by_column_name(self):
        """
        test the get_value_by_column_name method which accepts the following arguments:
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [0,base_df_cols[0],base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [base_df_values[0]]

        # cause a side effect to test
        test_result = self.test_client.get_value_by_column_name(
            *side_effect_input)

        # test that the side effect is expected
        self.assertEqual(test_result, side_effect_output[0])

    def test_side_effects_get_value_by_column_index(self):
        """
        test the get_value_by_column_index method which accepts the following arguments
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [0,0,base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [base_df_values[0]]

        # cause a side effect to test
        test_result = self.test_client.get_value_by_column_index(
            *side_effect_input)

        # test that the side effect is expected
        self.assertEqual(test_result, side_effect_output[0])

    def test_side_effects_delete_table(self):
        """
        test the delete_table method which accepts the following arguments
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [pd.DataFrame([])]

        # cause a side effect to test
        test_result = self.test_client.delete_table(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))
        
    def test_side_effects_append_row(self):
        """
        test the append_row method which accepts the following arguments
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [[121],base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [pd.DataFrame([*base_df_values, 121],columns=base_df_cols)]

        # cause a side effect to test
        test_result = self.test_client.append_row(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))

    def test_side_effects_delete_rows(self):
        """
        test the delete_rows method which accepts the following arguments
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [[0],base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [pd.DataFrame(base_df_values[1:],columns=base_df_cols)]
        # cause a side effect to test
        test_result = self.test_client.delete_rows(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))

    def test_side_effects_put_column(self):
        """
        test the put_column method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = ["new_col",base_df_values,base_table_name]
        # array containing the expected correct result of the side effect
        df= df = pd.DataFrame(base_df_values,columns=base_df_cols)
        df.insert(1,"new_col",base_df_values)
        side_effect_output = [df]

        # cause a side effect to test
        self.test_client.put_column(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))

    def test_side_effects_insert_column(self):
        """
        test the insert_column method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - None
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [0,"new_col",base_df_values,base_table_name]
        # array containing the expected correct result of the side effect
        df = df = pd.DataFrame(base_df_values,columns=base_df_cols)
        df.insert(0, "new_col", base_df_values)
        side_effect_output = [df]

        # cause a side effect to test
        self.test_client.insert_column(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))

    def test_side_effects_delete_columns(self):
        """
        test the delete_columns method which accepts the following arguments:

        ---
        Parameters:

        ---
        Returns:
        - Any
        """
        # array of arguments which are expected by the method which causes the side effect under test
        side_effect_input = [[base_df_cols[0]],base_table_name]
        # array containing the expected correct result of the side effect
        side_effect_output = [pd.DataFrame([])]

        # cause a side effect to test
        self.test_client.delete_columns(*side_effect_input)

        # test that the side effect is expected
        test_result = self.test_client.get_table(base_table_name)
        self.assertTrue(test_result.equals(side_effect_output[0]))
    
if __name__ == "__main__":
    unittest.main()
