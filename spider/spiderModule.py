# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 10:10:38 2018

@author: zmddzf
@description:
    This is a spider library which includes:
    URLmanager: a manager to control the URL queue
    WebParser: a Parser to get value data/URL
    WebDowloader: to download html
"""

from urllib import request
from spider import UA_POOL as UP
from queue import Queue
import re
import numpy as np
import pandas as pd


class URLmanager:
    """
    This is a queue to manage URL list
    attributes:
        URLlist: a list type
        isEmpty: descriminate the queue is empty or not
        getURL: pull URL from the queue
    """
    
    def __init__(self, URLlist):
        URL = set(URLlist)
        self.URLqueue = Queue()
        for url in URL:
            self.URLqueue.put(url)
        
    def isEmpty(self):
        return self.URLqueue.empty()
    
    def getURL(self):
        if self.URLqueue.empty():
            return False
        else:
            return self.URLqueue.get()

def webDownloader(URL):
    """
    This a function to download the html
    args:
        url: a string of url
    returns:
        data: a string of html
    """
    opener = request.build_opener()
    opener.addheaders = UP.getHEADER()
    request.install_opener(opener)
    data = request.urlopen(URL).read().decode("utf-8","ignore")
    data = data.replace('\n', '')
    return data

def webParser(html, pattern):
    """
    This is a function to match the information
    args:
        html: string type
        pattern: the re pattern
    returns:
        all matched information
    """
    return re.findall(pattern, html, re.S)

class StockSpider:
    """
    This is a class which is designed to get stock data
    attributes:
        __pattern1: private, a re pattern to get html table
        __pattern2: private, a re pattern to get stock data
        __pattern3: private, a re pattern to get table head
        stockData: a method to get stock data
    """
    
    __pattern1 = '<table class="table_bg001 border_box limit_sale">(.*?)<\/table>'
    __pattern2 = '\d+\.?\d*e?\d*?'
    __pattern3 = '<th>(.*?)</th>'
    def __init__(self, stockID, year, season):
        self.stockID = stockID
        self.year = year
        self.season = season
        self.URL = 'http://quotes.money.163.com/trade/lsjysj_%s.html?year=%s&season=%s'%(self.stockID,self.year,self.season)
    
    def __getTable(self):
        content = webDownloader(self.URL)
        self.table = webParser(content, self.__pattern1)[0].replace(',', '')
    
    def __getHead(self):
        self.head = webParser(self.table, self.__pattern3)
    
    def __getData(self):
        data = webParser(self.table, self.__pattern2)
        self.data = []
        date = ''
        for num, item in enumerate(data):
            if num % 13 <= 2:
                date += item
                if num % 13 == 2:
                    self.data.append(date)
                    date = ''
            else:
                self.data.append(item)
    
    def stockData(self):
        """
        This is a methods to fetch stock data
        First use 3 private methods to initiate,
        then change it to dict type
        returns:
            stock: a pandas.DataFrame type
        example:
            >>> stock = StockSpider('600218','2018','4')
            >>> data = stock.stockData()
            >>> print(data)
        """
        self.__getTable()
        self.__getHead()
        self.__getData()
        data = np.array(self.data)
        data = data.reshape(int(len(self.data)/len(self.head)), len(self.head)).T
        stock = {}
        for i, j in zip(self.head, data):
            stock[i] = j.tolist()
        stock = pd.DataFrame(stock)
        return stock
        
        
        
        
            
        
        