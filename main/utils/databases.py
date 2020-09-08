import os
import psycopg2
import json
import logging
import sys
import re
from typing import List


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

class PostgresConnection:

    def open_postgres_conn(self):
        with open("heroku_db_creds.json", 'r') as creds_file:
            creds = json.load(creds_file)
        conn = psycopg2.connect(**creds)
        return conn
    
    def close_postgres_conn(self):
        self.conn.close()
        return

    def insert_values_to_table(self, table_name, table_schema, values: List):
        values_str = str(values)
        values_str = re.sub("^\[", "(", values_str)
        values_str = re.sub("\]$", ")", values_str)

        try:
            conn = self.open_postgres_conn()
            curs = conn.cursor()
            SQL = """
                INSERT INTO {} VALUES {} 
                """.format(table_name, values_str)
            logger.info("Executing {sql}".format(sql=SQL))
            curs.execute(SQL)
            conn.commit()
        except psycopg2.errors.UndefinedTable:
            logger.error("psycopg2 UndefinedTable error was thrown. Creating table...")
            conn.close()
            conn = self.open_postgres_conn()
            curs = conn.cursor()
            SQL_CREATE_TABLE = self.generate_create_table_sql(table_name, table_schema)
            logger.info("Executing {sql}".format(sql=SQL_CREATE_TABLE))
            curs.execute(SQL_CREATE_TABLE)
            conn.commit()
            logger.info("Executing {sql}".format(sql=SQL))
            curs.execute(SQL)
            conn.commit()

        conn.close()

        return

    def generate_create_table_sql(self, table_name, schema):
        sql_list = []
        for k,v in schema.items():
            line_str = "{} {}".format(k,v)
            sql_list.append(line_str)
        sql_body = ",".join(sql_list)
        SQL_CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS {} (
            {} )
        """.format(table_name, sql_body)
        return SQL_CREATE_TABLE