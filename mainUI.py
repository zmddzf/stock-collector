from baseUI import Ui_stockData
import sys
import spider.spiderModule as sm
from PyQt5.QtWidgets import *
import spider.dbModule as dm
import sqlite3
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from generateFig import Figure_Canvas

class LogicalUI(QWidget, Ui_stockData):
    """
    This is a class for the service logic
    """
    def __init__(self, parent = None):
        super(LogicalUI, self).__init__(parent)
        self.setupUi(self)
        self.showMaximized()
        self.subInfo.clicked.connect(self.on_subinfo_clicked)
        self.chgFig.clicked.connect(self.on_chgFig_clicked)
        #self.toCsv.clicked.connect(self.on_toCsv_clicked)
        #self.toolButton.clicked.connect(self.on_toolButton_clicked)

    @pyqtSlot()
    def on_subinfo_clicked(self):
        """
        This is a method connected to the subinfo button
        get the input and crawl the data from the website
        show the data on the tableWidget and save it in the database
        """
        # Get user input from lineEditor
        stockID = self.stockID.text()
        year = self.year.text()
        quarter = str(self.quarter.currentIndex() + 1)

        # Check the input legal or not
        idCheck = ((len(stockID) == 6) and (stockID.isdigit()))
        yearCheck =(len(year) == 4) and year.isdigit() and (int(year) <= datetime.datetime.now().year)

        # If not pass, show information in the message box
        if not (idCheck and yearCheck):
            QMessageBox.critical(self, "信息错误", self.tr("请输入正确的信息！"))
        else:
            # Active spider to get data
            stockSp = sm.StockSpider(stockID, year, quarter)
            try:
                data = stockSp.stockData()
            except:
                QMessageBox.critical(self, "数据获取错误", self.tr("无法获取数据，请检查网络连接或所需股票信息!"))
            else:
                # Show data in the tableWidget
                self.tableWidget.setRowCount(len(data))
                header = ['日期', '开盘价', '收盘价', '最低价', '最高价', '成交量(手)', '成交金额(万元)', '换手率(%)', '振幅(%)', '涨跌幅(%)', '涨跌额']
                for i, head in enumerate(header):
                    for j, item in enumerate(data[head]):
                        self.tableWidget.setItem(j, i, QTableWidgetItem(item))

                # Save data into the sqlite
                conn = sqlite3.connect('stock.db')
                stockModel = dm.StockModel(conn)
                stockModel.to_db(data)

    @pyqtSlot()
    def on_toCsv_clicked(self):
        """
        This is the method connected to the toCsv button
        when clicked the button, the data will be saved int the csv file
        the file is in the written path
        """
        pth = self.path.text()
        print(pth)

        # Save data as .csv
        conn = sqlite3.connect('stock.db')
        stockModel = dm.StockModel(conn)
        stockModel.to_csv(pth)

    @pyqtSlot()
    def on_toolButton_clicked(self):
        """
        This is a method connected to the tool button
        Choose the path and set it the text of input line
        """
        pth = QFileDialog.getExistingDirectory(self, "选取文件夹","./")
        print(pth)
        self.path.setText(pth)

    @pyqtSlot()
    def on_chgFig_clicked(self):
        """
        This is a method connected to the chgFig button
        get the choice from user and draw different figure
        """
        # Get the choice of user
        figType = self.figType.currentIndex()

        # Connect to the database
        conn = sqlite3.connect('stock.db')
        stockModel = dm.StockModel(conn)

        # Read data from database and catch exception
        try:
            df = stockModel.query('SELECT * FROM STOCKSOURCE')
        except:
            QMessageBox.critical(self, "暂无数据", self.tr("暂无股票数据，请先爬取数据再进行绘图!"))

        # Initiate figure canvas
        date = df['日期']
        fc = Figure_Canvas()

        if figType == 0:
            start = df['开盘价'].astype(float)
            end = df['收盘价'].astype(float)
            high = df['最高价'].astype(float)
            low = df['最低价'].astype(float)
            fc.pricePlot(date, start, end, high, low)


        if figType == 1:
            fc.volumeHist(date, df['成交量(手)'].astype(float))

        if figType == 2:
            fc.exchangePlot(date, df['换手率(%)'].astype(float))

        if figType == 3:
            fc.ampPlot(date, df['振幅(%)'].astype(float))

        if figType == 4:
            fc.changePlot(date, df['涨跌额'].astype(float))

        # map the figure to UI
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fc)
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()



