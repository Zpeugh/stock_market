import intrinio
import requests
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
import numpy as np

class DataCollection:

    def __init__(self):
        self.ticker_symbols = []
        self.intrinio_username = '6a547746e6f8e7d3d58f24ab710b5a47'
        self.intrinio_password = '7978430efa72258cec86d6396ce505e4'
        self.data = []


    def _send_request(self, ticker_symbol=None, start_date=None):

        request = "https://api.intrinio.com/prices?identifier=%s&page_size=%d&start_date=%s&page_number=%d&item=price_close&item=price_date&frequency=weekly" % (ticker_symbol, 500, start_date, 1)
        req = requests.get(request, auth=HTTPBasicAuth(self.intrinio_username, self.intrinio_password))
        response = req.json()
        data = response['data']
        num_pages = response['total_pages']
        print("total pages: %d" % num_pages)
        if num_pages > 1:
            # TODO: Make these asynchronous calls
            for page in range(2, num_pages+1):
                request = "https://api.intrinio.com/prices?identifier=%s&page_size=%d&start_date=%s&page_number=%d&item=price_close&item=price_date&frequency=weekly" % (ticker_symbol, 500, start_date, page)
                req = requests.get(request, auth=HTTPBasicAuth(self.intrinio_username, self.intrinio_password))
                response = req.json()
                data.extend(response['data'])
                print "Response: \nresult_count: %d\npage_size: %d\Page: %d/%d" % (response['result_count'], response['page_size'], response['current_page'], response['total_pages'])

        return data


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
            self.data[key] = self._send_request(key, start_date)
        return self.data

    def plot_data(self, ticker_symbol):
        data = self.data[ticker_symbol]

        X = [x['date'] for x in data]
        Y = [y['close'] for y in data]
        x_range = np.arange(len(X))
        # plt.xticks(x_range, X)
        plt.plot(x_range, Y)
        plt.show()
