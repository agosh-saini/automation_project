from sqlite3 import connect

class relation_db:

    # initializing class
    def __init__(self, db_name, db_dir="database"):
        self.db_dir = db_dir
        self.db_name = db_name

    # connect to a db, if db does not exist, creat db
    def create_db(self, name=None, db_dir_update=None):

        # update dir if needed
        if db_dir_update is not None:
            self.db_dir = db_dir_update

        # update name if needed
        if name is not None:
            self.db_name = name

        # create db
        connection = connect(self.db_dir + '\\' + self.db_name)

        # exit
        connection.commit()
        connection.close()

        return self.db_dir, self.db_name

    # creating the index db
    def create_index_table(self, db_name=None, db_dir=None):

        # update dir if needed
        if db_dir is not None:
            self.db_dir = db_dir

        # update name if needed
        if db_name is not None:
            self.db_name = db_name

        # connect to index db and create cursor for communication
        connection = connect(self.db_dir + '\\' + self.db_name)
        cursor = connection.cursor()

        # create the DB
        cursor.execute(
            """ 
           CREATE TABLE IF NOT EXISTS test_summary (
               id INTEGER PRIMARY KEY,
               sensor_id INTEGER,
               metadata TEXT,
               gas TEXT,
               sensor TEXT,
               test_id TEXT KEY,
               date INTEGER
           ); 
           """
        )

        # exit
        connection.commit()
        connection.close()

    def add_to_index(self, sensor_id, metadata, gas, sensor, test_id, date):

        # connect to index db and create cursor for communication
        connection = connect(self.db_dir + '\\' + self.db_name)
        cursor = connection.cursor()

        # Insert data into the index table
        cursor.execute(""" 
            INSERT INTO test_summary
            (sensor_id, metadata, gas, sensor, test_id, date) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                       (sensor_id, metadata, gas, sensor, test_id, date))

        # exit
        connection.commit()
        connection.close()

    # creating the index db
    def create_table(self, test_id, db_name=None, db_dir=None):

        # update dir if needed
        if db_dir is not None:
            self.db_dir = db_dir

        # update name if needed
        if db_name is not None:
            self.db_name = db_name

        # connect to index db and create cursor for communication
        connection = connect(self.db_dir + '\\' + self.db_name)
        cursor = connection.cursor()

        # create the DB
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS " + test_id + """ (
               index FLOAT,
               sensor_id TEXT,
               time FLOAT,
               current_A FLOAT,
               resistance_Ohm FLOAT,
               stage TEXT,
               gas TEXT,
               concentration TEXT
                 
           ); 
           """
        )

        # exit
        connection.commit()
        connection.close()

    def add_to_table(self, test_id, df):

        # connect to index db and create cursor for communication
        connection = connect(self.db_dir + '\\' + self.db_name)
        cursor = connection.cursor()

        df.to_sql(test_id, connection, if_exists='replace')

        # exit
        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = relation_db("test.db")
    db.create_db()
    db.create_index_table()
    db.add_to_index(3, "test", "N2", "cuO", "A23A", 15)
    db.create_table("A23A")
    db.add_to_table("A23A", 3, 1.1, 1.2, 1.3, "stage", "1.4")
