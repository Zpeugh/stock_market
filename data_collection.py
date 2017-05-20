import intrinio
import requests
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import re

# def _pickle_method(method):
#     func_name = method.im_func.__name__
#     obj = method.im_self
#     cls = method.im_class
#     return _unpickle_method, (func_name, obj, cls)
#
# def _unpickle_method(func_name, obj, cls):
#     for cls in cls.mro():
#         try:
#             func = cls.__dict__[func_name]
#         except KeyError:
#             pass
#         else:
#             break
#     return func.__get__(obj, cls)
#
# import copy_reg
# import types
# copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

def _send_request(self, page_number, ticker_symbol, start_date=None):

    request = "https://api.intrinio.com/prices?identifier=%s&page_size=%s&start_date=%s&page_number=%s&item=price_close&item=price_date&frequency=weekly" % (ticker_symbol, 500, start_date, page_number)
    req = requests.get(request, auth=HTTPBasicAuth('6a547746e6f8e7d3d58f24ab710b5a47','7978430efa72258cec86d6396ce505e4'))
    response = req.json()
    print response
    # print "Response: \nresult_count: %s\npage_size: %s\Page: %s/%s" % (response['result_count'], response['page_size'], response['current_page'], response['total_pages'])
    return response['data']

def send_all_requests(args_list):
    return _send_request(*args_list)

class DataCollection:

    def __init__(self):
        self.ticker_symbols = []
        self.intrinio_username = '6a547746e6f8e7d3d58f24ab710b5a47'
        self.intrinio_password = '7978430efa72258cec86d6396ce505e4'
        self.data = dict()

    def _send_request(self, page_number, ticker_symbol, start_date=None):

        request = "https://api.intrinio.com/prices?identifier=%s&page_size=%s&start_date=%s&page_number=%s&item=price_close&item=price_date&frequency=weekly" % (ticker_symbol, 500, start_date, page_number)
        req = requests.get(request, auth=HTTPBasicAuth(self.intrinio_username, self.intrinio_password))
        response = req.json()
        # print "Response: \nresult_count: %s\npage_size: %s\Page: %s/%s" % (response['result_count'], response['page_size'], response['current_page'], response['total_pages'])
        return response['data']

    def _send_csv_request(self, ticker_symbol, start_date=None):

        request = "https://api.intrinio.com/historical_data.csv?identifier=%s&page_size=10000&start_date=%s&item=close_price&frequency=weekly" % (ticker_symbol, start_date)
        req = requests.get(request, auth=HTTPBasicAuth(self.intrinio_username, self.intrinio_password))
        return req.content


    def _get_first_page(self, ticker_symbol=None, start_date=None):
        request = "https://api.intrinio.com/prices?identifier=%s&page_size=%s&start_date=%s&page_number=%s&item=price_close&item=price_date&frequency=weekly" % (ticker_symbol, 500, start_date, 1)
        req = requests.get(request, auth=HTTPBasicAuth(self.intrinio_username, self.intrinio_password))
        response = req.json()
        data = response['data']
        num_pages = response['total_pages']
        print(data)
        return (num_pages, data)

    def _send_requests_async(self, ticker_symbol=None, start_date=None, n_cpu=4):

        num_pages, data = self._get_first_page(ticker_symbol, start_date)

        print "\n pages: %s" % num_pages
        args_list = []
        pool = Pool(n_cpu)

        for page in range(1, num_pages + 1):
            args_list.append( (page, ticker_symbol, start_date) )

        return pool.map(send_all_requests, args_list)

    def _is_data(self, line):
        is_data = True
        if line.find("RESULT_COUNT") is not -1:
            return False
        if line.find("PAGE_SIZE") is not -1:
            return False
        if line.find("total_pages") is not -1:
            return False
        if line.find("API_CALL_CREDITS") is not -1:
            return False
        if line.find("IDENTIFIER") is not -1:
            return False
        if line.find("DATE") is not -1:
            return False
        return is_data

    def _format_csv_data(self, data):
        lines = data.splitlines()
        print lines
        dates = []
        prices = []
        for line in lines[7:]:
            if self._is_data(line):
                pair = line.split(',')
                dates.append(pair[0])
                prices.append(pair[1])
        dates.reverse()
        prices.reverse()
        return dates, prices

    def get_prices(self, ticker_symbols=None, start_date=None):
        '''
            ticker_symbols:  the lookup for the stock ticker symbol.
                            For example, 'AAPL' for Apple.
            start_date:     string of 'YYYY-MM-DD' for first date to retrieve
                            the historical stock data from.
                            Defaults to Jan 1st, 1980.

        '''
        if start_date == None:
            start_date = '1980-01-01'
        elif len(str(start_date)) == 4:
            start_date = "%s-01-01" % start_date

        if ticker_symbols == None and len(self.ticker_symbols) < 0:
            print "No tickers available to retrieve prices for"
            return
        elif isinstance(ticker_symbols, str):
            print(self.ticker_symbols)
            self.ticker_symbols.append(ticker_symbols)

        self.data = dict()
        for key in self.ticker_symbols:
            # self.data[key] = self._send_requests_async(key, start_date, n_cpu=4)
            data = self._send_csv_request(key, start_date)
            self.data["%s_dates" % key], self.data["%s_prices" % key] = self._format_csv_data(data)
        return self.data

    def plot_data(self, ticker_symbol):
        X = self.data['%s_dates' % ticker_symbol]
        Y = self.data['%s_prices' % ticker_symbol]
        x_range = np.arange(len(X))
        x_ticks = np.arange(0,len(X), 25)
        date_labels = [X[i][:7] for i in x_ticks]
        fig = plt.figure(figsize=(18,10))
        plt.xticks(x_ticks, date_labels, rotation='vertical')
        plt.plot(x_range, Y)
        plt.xlabel("Dates")
        plt.ylabel("Close Price ($)")
        plt.title("Historical Data for %s" % ticker_symbol)
        plt.show()
