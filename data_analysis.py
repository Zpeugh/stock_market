import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr as pearson

class DataAnalysis():


    def __init__(self, dates=None, prices=None):
        self.dates = dates
        self.prices = prices


    def _find_top_yearly_trend(self, dates, prices, months_in_period):
        chunked_data = dict()
        i = 0
        for year in range(dates[0].year, dates[-1].year + 1):
            # Each year will have an array of (12 / months_in_period) datasets for the year
            chunked_data["%s" % year] = []

            date = dates[i]
        print chunked_data
        for i, date in enumerate(dates):
                if date.month == 1:
                    print date.year
                    print chunked_data[date.year]
                    # push index of January in the first spot of the year
                    chunked_data["%s" % date.year].append(i)
                if date.month % months_in_period == 0:
                    chunked_data["%s" % date.year].append(i)

        return chunked_data

    def get_yearly_trends(self, dates, prices, periods=None):
        '''
            data        Timeseries data with dates and prices
            periods     Array of monthly periods to examine
        '''

        if periods == None:
            periods = np.arange(1,13)

        if dates == None:
            dates = self.dates
            if data == None:
                print "No dates to perform trend analysis on!"
                return
        if prices == None:
            prices = self.prices
            if prices == None:
                print "No prices to perform trend analysis on!"
                return
        trends = dict();

        for period in periods:
            trends[period] = self._find_top_yearly_trend(dates, prices, period)

        return trends



    def plot_data(self, dates, prices, ticker_symbol, start_date=None):
        X = dates
        Y = prices
        x_range = np.arange(len(X))
        x_ticks = np.arange(0,len(X), 30)
        date_labels = [X[i].strftime("%B %Y") for i in x_ticks]
        fig = plt.figure(figsize=(18,10))
        plt.xticks(x_ticks, date_labels, rotation='vertical')
        plt.plot(x_range, Y)
        plt.xlabel("Dates")
        plt.ylabel("Close Price ($)")
        plt.title("Historical Data for %s" % ticker_symbol)
        plt.show()
