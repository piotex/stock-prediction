from charts import *
from data import *
from rsi import calculate_rsi

row_list = get_data_from_json()

stooq_date = [x["Date"] for x in row_list]
stooq_vals = [x["Close"] for x in row_list]

max_wallet_period = 4
max_percent_buy = 95
max_percent_sell = 10

walet_in_time = get_wallet_values_in_time(stooq_vals, max_wallet_period, 10000, max_percent_buy/100, max_percent_sell/100)
plot_chart_stock_rsi_wallet(stooq_date, stooq_vals, max_wallet_period, 10000, max_percent_buy/100, max_percent_sell/100)

print(f"Max wallet return: {walet_in_time[-1]}")

