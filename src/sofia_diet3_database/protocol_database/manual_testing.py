from exceldatabase import ExcelDatabase

if __name__ == "__main__":
  db = ExcelDatabase()
  db.create_table("my_routine", ["Week Day", "Expenses"], [
                  ["Monday", 0.5], ["Tuesday",0.2]])
  print(db.get_table("my_routine"))
  db.preview_table("my_routine")
