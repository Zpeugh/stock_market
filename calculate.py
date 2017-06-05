from data_collection import DataCollection
import sys
import matplotlib.pyplot as plt
import intrinio
from data_analysis import DataAnalysis

# USERNAME = '6a547746e6f8e7d3d58f24ab710b5a47'
# PASSWORD = '7978430efa72258cec86d6396ce505e4'

USERNAME = 'b45dbf1f518214c76085b7e67ec8dc31'
PASSWORD = '7ef892807d408fa2b7471ec3392ee80d'

data_collection = DataCollection(username=USERNAME, password=PASSWORD)

ticker_symbol = "AAPL"
dates, prices = data_collection.retrieve_data(ticker_symbol)
da = DataAnalysis()


# data = da.get_yearly_trends(dates, prices, [3])

bounds, sell_dates, profits = da.get_optimal_bounds(dates, prices, low_bound_min=0.3, top_bound_max=0.5, interval=0.01, investment=100, purchase_strategy="immediate")
da.plot_data(dates, prices, ticker_symbol, sell_dates=sell_dates)


# if sys.argv[1]:
#     ticker = sys.argv[1]
#     start_date = sys.argv[2]
#     results = data_collection.get_prices(ticker, start_date)
#     data_collection.plot_data(ticker)
#     data_collection.save_data(ticker)

# else:
# with open('nasdaq.csv') as ticker_symbols:
#     for line in ticker_symbols:
#         ticker = line.strip()
#         results = data_collection.get_prices(ticker, 1980)
#         data_collection.save_data(ticker)
