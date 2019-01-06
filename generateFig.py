import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import mpl_finance as mpf
from matplotlib.pylab import date2num


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=30, height=4, dpi=100):

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure
        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)
        self.axes = fig.add_subplot(111)  # 调用figure下面的add_subplot方法

    def pricePlot(self, date, start, end, high, low):
        """
        Draw k-line chart.
        :param date: stock date, a pd series type
        :param start: open price, a pd series type
        :param end: closed price, a pd series type
        :param high: the highest price, a pd series type
        :param low: the lowest price, a pd series type
        :return: None
        """
        date = pd.to_datetime(date)
        date1 = date.apply(lambda x: date2num(x))
        data = pd.concat([date1, start, end, high, low], axis=1)
        data_mat = data.as_matrix()
        self.axes.xaxis_date()
        self.axes.set_xlabel("时间")
        self.axes.grid(True)
        self.axes.set_ylabel("股价（元）")
        mpf.candlestick_ochl(self.axes, data_mat, width=0.6, colorup='g', colordown='r', alpha=1.0)

    def volumeHist(self, date, data):
        """
        Draw volume bar chart.
        :param date: stock date, a pd series type
        :param data: deal volume, a pd series type
        :return: None
        """
        date = pd.to_datetime(date)
        date = date.apply(lambda x: date2num(x))

        self.axes.xaxis_date()
        self.axes.set_xlabel("时间")
        self.axes.set_ylabel("成交量（手）")
        self.axes.bar(date, data, width=0.5)


    def exchangePlot(self, date, data):
        """
        Draw exchange rate plot.
        :param date: stock date, a pd series type
        :param data: stock exchange rate, a pd series type
        :return:
        """
        date = pd.to_datetime(date)
        self.axes.xaxis_date()
        self.axes.set_xlabel("时间")
        self.axes.set_ylabel("换手率")
        self.axes.plot(date, data)

    def ampPlot(self, date, data):
        """
        Draw stock amplitude plot
        :param date: stock date, a pd series type
        :param data: stock amplitude plot, a pd series type
        :return: None
        """
        date = pd.to_datetime(date)
        self.axes.xaxis_date()
        self.axes.set_xlabel("时间")
        self.axes.set_ylabel("振幅(%)")
        self.axes.plot(date, data)

    def changePlot(self, date, data):
        """
        Draw the stock amount of change plot
        :param date: stock date, a pd series type
        :param data: amount of change, a pd series type
        :return: None
        """
        date = pd.to_datetime(date)
        self.axes.xaxis_date()
        self.axes.set_xlabel("时间")
        self.axes.set_ylabel("涨跌额")
        self.axes.plot(date, data)

