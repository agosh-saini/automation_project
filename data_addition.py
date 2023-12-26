'''
Name: Agosh Saini
Email: as7saini@uwaterloo.ca
---
This is the document used for preprocessing the data
'''

from numpy import array
from os import path
from sqlite3 import connect
import logging
from pandas import read_sql_query


class data_addition:
    def __int__(self, dbpath, files="*"):
        if isinstance(files, str):
            logging.error("need to be a SQL query as string")
            raise TypeError("need to be a SQL query as string")

        if not path.isfile(dbpath):
            logging.error("not a valid path to sqllite db")
            raise TypeError("not a valid path to sqllite db")

        self.dbpath = dbpath
        self.file_query = files
        self.con = None
        self.cur = None

    def connection(self):
        con = connect(self.dbpath)
        cur = con.cursor()

        logging.info("Connection with SQLLite DB established")

        return con, cur

    def get_test_list(self, custom_query=False):

        con, cur = self.connection()

        if custom_query and not isinstance(custom_query, str):
            logging.error("Need query in string form")
            raise TypeError("Need query in string form")

        query = """SELECT test_id FROM test_summary"""

        if custom_query:
            query = custom_query

        list_of_data = read_sql_query(query, con)

        con.commit(), cur.close(), con.close()

        logging.info("fetched query results and closed sql connection")

        return list_of_data

    def get_file(self, test_id, custom_query=False):

        con, cur = self.connection()

        if custom_query and not isinstance(custom_query, str):
            logging.error("Need query in string form")
            raise TypeError("Need query in string form")

        query = """SELECT resistance_Ohm, json_extract(gas), 
                    json_extract(concentration) from {tn}""".format(tn=test_id)

        if custom_query:
            query = custom_query

        data = read_sql_query(query, con)

        con.commit(), cur.close(), con.close()

        logging.info("returned data from {tn}".format(tn=test_id))

        return data


