from charts import *
from data import *
from rsi import calculate_rsi

download_data = False
download_data = True
if download_data:
    stock_index = "usdpln"
    stock_index = "eurpln"
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


period = 14
plot_chart_stock_rsi_wallet(stooq_date, stooq_vals)


