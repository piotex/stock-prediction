import requests
import datetime

from rsi.calculate_rsi import calculate_rsi
from rsi.functions import url_generator, parse_stock_data
from rsi.plot_charts import plot_charts
from rsi.simulate_strategy import simulate_strategy

read_from_stooq = True
# stock_index = "usdpln" # U.S. Dollar / Polish Zloty (USDPLN)
stock_index = "pkn" # ORLEN SA (PKN)

file_in = "usd-pln.txt"
row_list = []
data_vals = []


if read_from_stooq:
    now = datetime.datetime.now()
    yyyy_mm_dd = f"{now.year:04d}{now.month:02d}{now.day:02d}"
    interval = "d"  # "240"=4h     "d"

    url = url_generator(stock_index, interval, yyyy_mm_dd)
    print(url)
    resp = requests.get(url)
    with open(file_in, "w", newline="", encoding="utf-8") as f:
        f.writelines(resp.text)
        row_list = parse_stock_data(resp.text)
else:
    with open(file_in, "r", newline="", encoding="utf-8") as f:
        data = f.read()
        row_list = parse_stock_data(data)

# row_list = row_list[:70]

vals_list = [x["Close"] for x in row_list]
date_vals = [x["Date"] for x in row_list]
rsi_vals = calculate_rsi(vals_list, period=rsi_period)

buy_threshold = 30
sell_threshold = 70

buy_vals = []
sell_vals = []
for val in rsi_vals:
    if val is None:
        buy_vals.append(2)
        sell_vals.append(0)
        continue

    if val < buy_threshold:
        buy_vals.append(1)
    else:
        buy_vals.append(0)

    if val > sell_threshold:
        sell_vals.append(1)
    else:
        sell_vals.append(0)


portfolio_values = simulate_strategy(vals_list, buy_vals, sell_vals,
                                     initial_cash=10000,
                                     buy_amount_pln=1500,
                                     sell_amount_pln=1500)

plot_charts(date_vals, vals_list, rsi_vals, buy_vals, sell_vals, portfolio_values)







