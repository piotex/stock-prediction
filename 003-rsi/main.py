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



max_wallet_val = 0
max_wallet_period = 0
for i in range(1, 30):
    walet_in_time = get_wallet_values_in_time(stooq_vals, i)
    if max_wallet_val < walet_in_time[-1]:
        max_wallet_val = walet_in_time[-1]
        max_wallet_period = i
print(f"Max wallet return: {max_wallet_val}")
print(f"For period: {max_wallet_period}")

plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, max_wallet_period)
