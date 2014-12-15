#!/usr/bin/env python3

""" A program that performs data mining on the price of stock data."""

__author__ = 'Joanna Kolbe, Shuai Wang'
__email__ = "joannakolbe@gmail.com, info.shuai@gmail.com"
__copyright__ = "2014 Joanna Kolbe, Shuai Wang"
__status__ = "Prototype"

# imports one per line
import json
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


class Stock:
    """
    Class for stock data.
    """

    def __init__(self, stock_name, stock_file_name):
        """
        (Stock, str, str) -> NoneType
        Creates a new Stock object with stock_name from stock_file_name, and
        initializes some variables.
        """
        self.stock_name = stock_name
        self.stock_file_name = stock_file_name
        self.stock_data = []
        self.months = {}
        self.monthly_averages = []

        # some method calls for later use
        self.read_json_from_file()
        self.initialize_months()
        self.calculate_average()
        self.sort_by_price()

    def average(self):
        """
        Getter: returns monthly averages of the stock

        :return: a list: monthly averages of the stock
        """
        return self.monthly_averages

    def name(self):
        """
        Getter: returns the name of the stock

        :return: a string: the name of the stock
        """
        return self.stock_name

    def span(self):
        """
        Getter: returns the span of the stock.

        :return: int, the span of the stock.
        """
        return len(self.months)

    def read_json_from_file(self):
        """
        Reads json file specified by stock_file_name and
        initializes stock_data content.
        """
        with open(self.stock_file_name) as file_handle:
            file_contents = file_handle.read()
        self.stock_data = json.loads(file_contents)

    def initialize_months(self):
        """
        Populates months (a dict where key being YYYY/MM and
        value being a list of stock objects) with all data
        associated with specific month found in the stock file.
        """
        if type(self.stock_data) is not list:
            raise TypeError("Invalid stock data")

        for stock in self.stock_data:
            if type(stock) is not dict:
                raise TypeError("Invalid stock in stock data")
            if ("Date" in stock.keys() and
               self.valid_date_format(stock["Date"])):
                # format date to YYYY/mm
                YYYY, mm, dd = stock["Date"].split("-")
                date = YYYY + "/" + mm
                self.months.setdefault(date, []).append(stock)
            else:
                raise ValueError("Date of stock not provided or invalid")

    def calculate_average(self):
        """
        Calculates average for each month in months dict, and
        stores tuples (month, average) in monthly_averages list.
        """
        if type(self.months) is not dict:
            raise TypeError("Months is not of type dictionary")
        if len(self.months) == 0:
            raise ValueError("Months not initialized")

        for (date, obj_list) in self.months.items():
            numerator = 0       # will hold the sum (v1*c1 + ... + vn+cn)
            denominator = 0     # will hold the sum (v1+...+vn)
            if type(obj_list) is not list:
                raise TypeError("Unexpected months value format")
            for stock in obj_list:
                # check if close and volume exist
                if "Close" in stock.keys() and "Volume" in stock.keys():
                    # check for type
                    if (type(stock["Volume"]) is int
                       and type(stock["Close"]) in [int, float]):
                        numerator += stock["Volume"] * stock["Close"]
                        denominator += stock["Volume"]
                    else:
                        raise TypeError("Invalid attribute type of stock")
                else:
                    raise ValueError("Data missing")

            average = round(numerator / denominator, 2)
            self.monthly_averages.append((date, average))

    def sort_by_price(self):
        """
        Sorts monthly_averages list of tuples of format (string, float) by
        price in aescending order (lowest first).
        """
        self.monthly_averages.sort(key=lambda x: x[1])

    def sort_by_time(self):
        """
        Sorts monthly_averages list of tuples of format (string, float) by
        time in aescending order (earliest first).
        """
        self.monthly_averages.sort(key=lambda x: x[0])

    def six_best_months(self):
        """
        Retrieves 6 highest stock averages in a certain period.

        :return: a list of tuples(date, float)
        """
        if len(self.monthly_averages) < 6:
            raise ValueError("Not enough months")
        best_six = self.monthly_averages[-6:]
        return best_six[::-1]   # reverse descending order

    def six_worst_months(self):
        """
        Retrieves 6 lowest stock averages in a certain period.

        :return: a list of tuples(date, float)
        """
        if len(self.monthly_averages) < 6:
            raise ValueError("Not enough months")
        return self.monthly_averages[:6]

    @staticmethod
    def valid_date_format(date):
        """
        Checks whether a date has the format YYYY-mm-dd in numbers

        :param date: date to be checked
        :return: Boolean True if the format is valid; False otherwise
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def visualize(self):
        """
        Visualizes the average monthly stock price over time, and also
        marks the best six months and worst six months.
        """
        self.sort_by_time()     # sort by time for time series plot
        time = [self.monthly_averages[i][0] for i in range(self.span())]
        price = [self.monthly_averages[i][1] for i in range(self.span())]

        datetime_list = list()
        for i in range(len(time)):
            YYYY, mm = time[i].split("/")
            datetime_list.append(datetime.datetime(int(YYYY), int(mm), 15))

        # numpy array
        datetime_arr = np.array(datetime_list)
        price_arr = np.array(price)

        # find indices of the best six and worse six months for markers
        best_indices = sorted(range(len(price)), key=lambda i: price[i])[-6:]
        worst_indices = sorted(range(len(price)), key=lambda i: price[i])[:6]

        # find the best six and worst six points
        best_six_time = datetime_arr[best_indices]
        best_six_price = price_arr[best_indices]
        worst_six_time = datetime_arr[worst_indices]
        worst_six_price = price_arr[worst_indices]

        # plot
        plt.plot(datetime_arr, price)
        plt.plot(best_six_time, best_six_price, "gD", label="Best six months")
        plt.plot(worst_six_time, worst_six_price, "rD",
                 label="Worst six months")

        plt.title(self.name() + " stock price over time")
        plt.xlabel("Time")
        plt.ylabel("Stock price ($)")
        plt.grid()
        plt.legend(loc="best", numpoints=1, prop={"size": 10})

    def gui(self):
        """
        Creates a graphical user interface for the stock.
        """
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        def print_best_six():
            print("Best six monthly averages (month, stock price)"
                  " for {0} are:".format(self.name()))
            for item in self.six_best_months():
                print(item)

        def print_worst_six():
            print("Worst six monthly averages (month, stock price)"
                  " for {0} are:".format(self.name()))
            for item in self.six_worst_months():
                print(item)

        def visual():
            self.visualize()

        # create label and buttons
        self.label_note = tk.Label(self.frame,
                                   text="Note: After hitting one of the three"
                                        " 'show' buttons, hit 'Quit' to see"
                                        " the results")
        self.button_best = tk.Button(self.frame, text="Show best",
                                     command=print_best_six)
        self.button_worst = tk.Button(self.frame, text="Show worst",
                                      command=print_worst_six)
        self.button_visualize = tk.Button(self.frame, text="Show plot",
                                          command=visual)
        self.button_quit = tk.Button(self.frame, text="Quit",
                                     command=self.frame.quit)

        # packing makes visible
        self.label_note.pack()
        self.button_best.pack()
        self.button_worst.pack()
        self.button_visualize.pack()
        self.button_quit.pack()

        # enters the Tk event loop
        self.root.mainloop()
        # destroys the main window when the event loop is terminated
        self.root.destroy()


def stdev(alist):
    """
    Given a list of numbers, computes its standard deviation.

    :param: alist: a list of numbers
    :return: the standard deviation of a list of numbers
    """
    if len(alist) == 0:
        raise ValueError("No value in the list")
    for stock_price in alist:
        if stock_price < 0:
            raise ValueError("Stock price can't be negative")

    mean = sum(alist) / len(alist)
    sum_square_deviation = sum((x - mean)**2 for x in alist)
    return math.sqrt(sum_square_deviation / len(alist))


def compare_stocks(stock1, stock2):
    """
    Takes two stocks objects, stock1 and stock2, and compares which of
    the two has the higher standard deviation of monthly averages.

    :param: stock1: one stock object
    :param: stock2: another stock object
    :return: the name of the stock that has higher standard deviation; or
        a message saying the two stocks have the same standard deviation
        if so.
    """
    stock1_ave = [stock1.average()[i][1] for i in range(stock1.span())]
    stock2_ave = [stock2.average()[i][1] for i in range(stock2.span())]

    if stdev(stock1_ave) > stdev(stock2_ave):
        return ("{0} stock has a higher standard deviation in monthly averages"
                " than that of {1}".format(stock1.name(), stock2.name()))
    elif stdev(stock1_ave) < stdev(stock2_ave):
        return ("{0} stock has a higher standard deviation in monthly averages"
                " than that of {1}".format(stock2.name(), stock1.name()))
    else:
        return ("{0} and {1} stocks have the same standard deviation"
                " in monthly averages".format(stock1.name(), stock2.name()))
