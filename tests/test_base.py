import unittest
from exceldatabase import ExcelDatabase
import pandas as pd

folder_name = "test_sofia_diet3_backend"
base_df_values = [1, 2, 3, 4, 5, 65]
base_df_cols = ["test_col1"]
base_df = pd.DataFrame(base_df_values, columns=base_df_cols)
base_table_name = "test_table"
another_df_cols = ["another_col"]
another_df_values = [0, 1, 1, 1, 1, 1]
another_df = pd.DataFrame(another_df_values, columns=another_df_cols)
another_table_name = "another_test_table"

print("Testing:" + ExcelDatabase.__doc__)


class Test_ExcelDatabase(unittest.TestCase):

    def setUp(self):
        self.test_client = ExcelDatabase()
        self.test_client.create_database(folder_name)
        self.test_client.set_folder_name(folder_name)
        self.test_client.create_table(
            base_table_name, base_df_cols, base_df_values)

    def tearDown(self):
        self.test_client.delete_database(folder_name)


if __name__ == "__main__":
    unittest.main()
