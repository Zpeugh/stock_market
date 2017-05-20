from data_collection import DataCollection
import sys
import matplotlib.pyplot as plt
import intrinio

intrinio.username = '6a547746e6f8e7d3d58f24ab710b5a47'
intrinio.password = '7978430efa72258cec86d6396ce505e4'


#
data_collection = DataCollection()
ticker = sys.argv[1]
start_date = sys.argv[2]

results = data_collection.get_prices(ticker, start_date)

print(len(results))

print(results.__class__)
data_collection.plot_data(ticker)
# print len(data_collection.data[ticker])
#
# data = data_collection.get_prices()['data']
#
# prices = [x['close'] for x in data]
#
#
# plt.plot(prices)
# plt.show()

# import pandas as pd
# import datetime
# import pandas_datareader as pdr
# import pandas_datareader.data as web
#
# start = datetime.datetime(1980,1,1)
# end = datetime.date.today()
#
# # apple = pdr.get_data_yahoo(sys.argv[1])
#
# data = web.DataReader(sys.argv[1], "yahoo", start, end)
#
# data['Close'].plot()
# plt.show()
# # apple['close'].plot(grid= True)
#
# # TODO: Compare monthly differentials/ highs and lows per year and find trends
# #       that are the most consistent in companies.
