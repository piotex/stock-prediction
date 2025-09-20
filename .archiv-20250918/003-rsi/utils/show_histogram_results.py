from charts import plot_chart_stock_rsi_histogram_wallet
from data import get_data_from_stock

with open('files/good_companies.txt', 'r') as file:
    data = file.readlines()
data = [a.strip() for a in data]

for idx, line in enumerate(data):
    interval = "d"
    stock_index = line.strip()
    try:
        row_list = get_data_from_stock(stock_index, interval)
    except Exception as eeee:
        continue

    stooq_date = [x["Date"] for x in row_list]
    stooq_vals = [x["Close"] for x in row_list]

    plot_chart_stock_rsi_histogram_wallet(stooq_date, stooq_vals)