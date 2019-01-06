# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 11:33:07 2018

@author: zmddzf
"""
import sqlite3 as lite
from pandas.io import sql

class StockModel:
    """
    This is a class to operate sqlite database
    attributes:
        to_db: save DataFrame into database
        query: send sql query to the database
        to_csv: fetch data from database and save it in csv file
    """
    
    def __init__(self, conn):
        self.conn = conn
    
    def to_db(self, df):
        """
        This is a method to save DataFrame into database
        args:
            df: pandas.DataFrame type
        returns:
            1 or -1
        """
        try:
            sql.to_sql(df, name = 'stockSource', con = self.conn, if_exists='replace')
        except:
            return -1
        else:
            return 1
        
    def query(self, sqlOrder):
        """
        send sql order to database in order to make query
        args:
            sqlOrder: string type, sql query order
        returns:
            result: pandas.DataFrame type
        """
        result = sql.read_sql(sqlOrder, self.conn)
        return result
    
    def to_csv(self, path):
        """
        query the database to get data and save it into the csv
        args:
            path: target file's path
        return:
            -1 or 1
        """
        df = self.query('SELECT * FROM STOCKSOURCE')
        try:
            df.to_csv(path, index = False, encoding = 'gbk')
        except:
            return -1
        else:
            return 1
