import sqlite3

'''
The SQLite implementation can be overridden for other database management system

Design considerations

sqlite3 also offers a context handler, BUT

a) you have to manage row_factory and cursor repetitively in the application code...
with sqlite3.Connection(db_path) as db:
    db.row_factory = sqlite3.Row        # boilerplate
    cursor = db.cursor()                # boilerplate
    cursor.execute(sql_statement)
    for row in cursor:
        print(row["author_id"])


b) and it does NOT close connections on __exit__
c = db.cursor()
c.execute(sql_statement)
for row in c:
    print(row["author_id"])
'''


class DatabaseClient:
    """
    A minimal sqlite3 context handler that removes pretty much all
    boilerplate code from the application level.

    * The connection - property is an instance of a sqlite3.Connection of the the client connection
    which can be used to commit the various statements
    * The cursor - is an sqlite.Cursor object which can be used to execute the sql statements
    """

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        # do not forget this or you will not be able to use methods of the
        # context handler in your with block
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


