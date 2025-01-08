import time
from charts import *
from data import *
from rsi import calculate_rsi
from tabulate import tabulate

from wallet import get_wallet_values_from_histogram_in_time

download_data = False
download_data = True
if download_data:
    stock_index = "eurpln"
    stock_index = "usdpln"
    stock_index = "xtb"
    stock_index = "pkn"
    interval = "d"              # d, w

    row_list = get_data_from_stock(stock_index, interval)
    save_data_to_json(row_list)
else:
    row_list = get_data_from_json()

stooq_date = [x["Date"] for x in row_list]
stooq_vals = [x["Close"] for x in row_list]
# stooq_vals = stooq_vals[:540]
# print(stooq_vals[:3])

# plot_chart(stooq_date, stooq_vals)
# plot_chart_stock_rsi(stooq_date, stooq_vals)
# plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, 14)


# start_time = time.time()
# print(f"{idx+1}/{len(stooq_vals_main_list)} | Czas wykonania: {int((time.time() - start_time) // 60)} min - {int((time.time() - start_time) % 60)} sek")

percent_buy = 30
percent_sell = 30

# for period in range(1, 30, 1):
#     walet_in_time = get_wallet_values_in_time(stooq_vals, period, 10000, percent_buy/100, percent_sell/100)

# plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, 14, 10000, percent_buy/100, percent_sell/100)
# plot_multichart_stock_rsi_wallet(stooq_date, stooq_vals, 14, 10000, percent_buy/100, percent_sell/100)
# plot_chart_stock_rsi_histogram(stooq_date, stooq_vals)

# days_in_past = 35
# stooq_date = stooq_date[-days_in_past:]
# stooq_vals = stooq_vals[-days_in_past:]
plot_chart_stock_rsi_histogram_wallet(stooq_date, stooq_vals)





