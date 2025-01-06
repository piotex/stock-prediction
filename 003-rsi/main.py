import time
from charts import *
from data import *
from rsi import calculate_rsi

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
print(stooq_vals[:3])

# plot_chart(stooq_date, stooq_vals)
# plot_chart_stock_rsi(stooq_date, stooq_vals)
# plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, 14)


max_period_const = 30
max_wallet_val = 0
max_wallet_period = 0
max_percent_buy = 0
max_percent_sell = 0

total_start_time = time.time()
start_time = time.time()
for period in range(1, max_period_const):
    for percent_buy in range(1,100,5):
        for percent_sell in range(1,100,5):
            walet_in_time = get_wallet_values_in_time(stooq_vals, period, 10000, percent_buy/100, percent_sell/100)
            if max_wallet_val < walet_in_time[-1]:
                max_wallet_val = walet_in_time[-1]
                max_wallet_period = period
                max_percent_buy = percent_buy
                max_percent_sell = percent_sell

    print(f"{period}/{max_period_const} | Czas wykonania: {int((time.time() - start_time) // 60)} min - {int((time.time() - start_time) % 60)} sek")
    start_time = time.time()
print(f"=== Total time: {int((time.time() - total_start_time) // 60)} min - {int((time.time() - total_start_time) % 60)} sek")

print(f"max_percent_buy: {max_percent_buy}")
print(f"max_percent_sell: {max_percent_sell}")
print(f"Max wallet return: {max_wallet_val}")
print(f"For period: {max_wallet_period}")

plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, max_wallet_period, 10000, max_percent_buy/100, max_percent_sell/100)
