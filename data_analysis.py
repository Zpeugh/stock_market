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
            dates       Array of datetime objects
            prices      Array of floats corresponding to dates
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



    def _price_is_within_bounds(self, purchase_price, current_price, low_bound, top_bound):
        if current_price < purchase_price:
            if current_price < purchase_price * (1 - low_bound):
                return False
            else:
                return True
        elif current_price > purchase_price:
            if current_price > purchase_price * (1 + top_bound):
                return False
            else:
                return True
        else:
            return True


    def _percent_profit(self, purchase_price, sell_price):
        return (sell_price - purchase_price) / purchase_price;

    def get_optimal_bounds(self, dates, prices, low_bound_min=0.3, top_bound_max=0.5, interval=0.01, investment=100, purchase_strategy="immediate"):
        '''
            dates           Array of datetime objects
            prices          Array of floats corresponding to dates
            low_bound_min   The percentage to allow a stock to decrease to before selling
            top_bound_max   The percentage to allow a stock to increase to before selling
        '''

        top_bounds = np.arange(0, top_bound_max + interval, interval)
        low_bounds = np.arange(0, low_bound_min + interval, interval)

        total_gain = 0
        profit_array = []
        final_sell_dates = []
        best_profit = -99999
        best_bounds = None
        purchase_price = float(prices[0])

        if purchase_strategy == "immediate":
            for top_bound in top_bounds:
                for low_bound in low_bounds:
                    profit_percentages = []
                    sell_dates = []
                    for index, price in enumerate(prices):
                        price = float(price)
                        if not self._price_is_within_bounds(purchase_price, price, low_bound, top_bound):
                            profit_percentages.append(self._percent_profit(purchase_price, price))
                            purchase_price = price
                            sell_dates.append(dates[index])
                    total_profit = np.sum(profit_percentages)
                    if total_profit > best_profit:
                        best_profit = total_profit
                        best_bounds = (low_bound, top_bound)
                        profit_array = profit_percentages
                        final_sell_dates = sell_dates
        return best_bounds, final_sell_dates, profit_percentages

    def plot_data(self, dates, prices, ticker_symbol, start_date=None, sell_dates=None):
        X = dates
        Y = prices
        x_range = np.arange(len(X))
        x_ticks = np.arange(0,len(X), 30)
        date_labels = [X[i].strftime("%B %Y") for i in x_ticks]
        fig = plt.figure(figsize=(18,10))
        plt.xticks(x_ticks, date_labels, rotation='vertical')
        plt.plot(x_range, Y)
        if sell_dates:
            date_indices = [dates.index(date) for date in sell_dates]
            for sell_date in date_indices:
                plt.axvline(x=sell_date, color="r")
        plt.xlabel("Dates")
        plt.ylabel("Close Price ($)")
        plt.title("Historical Data for %s" % ticker_symbol)
        plt.show()
