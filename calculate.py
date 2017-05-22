from data_collection import DataCollection
import sys
import matplotlib.pyplot as plt
import intrinio

# USERNAME = '6a547746e6f8e7d3d58f24ab710b5a47'
# PASSWORD = '7978430efa72258cec86d6396ce505e4'

USERNAME = 'b45dbf1f518214c76085b7e67ec8dc31'
PASSWORD = '7ef892807d408fa2b7471ec3392ee80d'

data_collection = DataCollection(username=USERNAME, password=PASSWORD)

if sys.argv[1]:
    ticker = sys.argv[1]
    start_date = sys.argv[2]
    results = data_collection.get_prices(ticker, start_date)
    data_collection.plot_data(ticker)
    data_collection.save_data(ticker)

# else:
# with open('nasdaq.csv') as ticker_symbols:
#     for line in ticker_symbols:
#         ticker = line.strip()
#         results = data_collection.get_prices(ticker, 1980)
#         data_collection.save_data(ticker)
