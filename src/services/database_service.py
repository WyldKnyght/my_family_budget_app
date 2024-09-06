# src/services/database_service.py

import sqlite3
from sqlite3 import Error
from utils.custom_logging import logger
from data_structures.pdf_info import PDFInfo
from configs.app_config import DATABASE_NAME

class DatabaseService:
    def __init__(self, db_file=DATABASE_NAME):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            logger.info(f"Successfully connected to database: {self.db_file}")
            return self.conn
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
        return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            logger.info("Table created successfully")
        except Error as e:
            logger.error(f"Error creating table: {e}")

    def insert_pdf_info(self, pdf_info: PDFInfo):
        table = "pdf_info"
        data = pdf_info.to_dict()
        placeholders = ', '.join(['?' for _ in data])
        columns = ', '.join(data.keys())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, list(data.values()))
            self.conn.commit()
            logger.info(f"Successfully inserted data for PDF: {pdf_info.filename}")
            return cur.lastrowid
        except Error as e:
            logger.error(f"Error inserting data: {e}")
            return None

    def fetch_pdf_info(self, condition=None):
        table = "pdf_info"
        sql = f"SELECT * FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [PDFInfo.from_dict(dict(zip([column[0] for column in cur.description], row))) for row in rows]
        except Error as e:
            logger.error(f"Error fetching data: {e}")
            return None

    def create_pdf_info_table(self):
        sql_create_pdf_info_table = """ CREATE TABLE IF NOT EXISTS pdf_info (
                                            id integer PRIMARY KEY,
                                            filename text NOT NULL,
                                            branch_address text,
                                            our_address text,
                                            statement_period text,
                                            account_summary text,
                                            additional_info text
                                        ); """
        self.create_table(sql_create_pdf_info_table)

    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()