import requests
import datetime
import os
import time
import random
from calculate_rsi import calculate_rsi
from functions import url_generator, parse_stock_data
from plot_charts import plot_charts, plot_charts_rsi
from plot_charts import plot_charts_rsi_trend_br
from values import *
from simulate_strategy import simulate_strategy


files = [f"{dir_name}/{x}" for x in os.listdir(dir_name)]
# files = [f"{dir_name}/wig20.txt"]

row_list = []
data_vals = []

# ================================== GET DATA ===============================================
indexes = []
for file in files:
    with open(file) as f:
        data = f.readlines()
        indexes += [x.strip() for x in data]

if read_from_stooq:
    now = datetime.datetime.now()
    yyyy_mm_dd = f"{now.year:04d}{now.month:02d}{now.day:02d}"
    interval = "d"  # "240"=4h     "d"

    for f in os.listdir("stocks"):
        os.remove("stocks/" + f)

    for i, index in enumerate(indexes):
        url = url_generator(index, interval, yyyy_mm_dd)
        time.sleep(random.uniform(1, 2))
        resp = requests.get(url)
        with open(f"stocks/{index}.txt", "w", newline="", encoding="utf-8") as f:
            f.writelines(resp.text)
        print(f"Downloaded {i+1} of {len(indexes)}")

# ================================== CALCULATE RSI ===============================================
results = []
dir_name = "stocks"
stocks_files = [f"{dir_name}/{x}" for x in os.listdir(dir_name)]
for stocks_file in stocks_files:
    with open(stocks_file, "r", newline="", encoding="utf-8") as f:
        try:
            row_list = parse_stock_data(f.read())
        except Exception as e:
            print(e)
            print(stocks_file)
            continue

    row_list = row_list[dates_to_parse:]
    vals_list = [x["Close"] for x in row_list]
    date_vals = [x["Date"] for x in row_list]

    portfolio_values = simulate_strategy(vals_list, initial_cash, initial_stock_value, buy_amount_pln, sell_amount_pln)

    end_value = portfolio_values[-1]
    min_value = min(portfolio_values)
    max_value = max(portfolio_values)
    index_name = os.path.splitext(os.path.basename(stocks_file))[0]

    results.append([index_name, end_value, min_value, max_value])





# ================================== PRINT DATA ===============================================
by_end = sorted(results, key=lambda x: x[1], reverse=True)  # po End Value
by_min = sorted(results, key=lambda x: x[2], reverse=True)  # po Min
by_max = sorted(results, key=lambda x: x[3], reverse=True)  # po Max

def write_table(f, title, rows):
    f.write(title + "\n")
    f.write(f"{'Index':<10} {'End Value':>12} {'Min':>12} {'Max':>12}\n")
    f.write("-" * 50 + "\n")
    for index_name, end_value, min_value, max_value in rows:
        f.write(f"{index_name:<10} {end_value:>12.2f} {min_value:>12.2f} {max_value:>12.2f}\n")
    f.write("\n\n")

with open("wyniki.txt", "w", encoding="utf-8") as f:
    write_table(f, "==== Posortowane po: End Value ====", by_end)
    write_table(f, "==== Posortowane po: Max ====", by_max)
    write_table(f, "==== Posortowane po: Min ====", by_min)

# dir_name = "stocks"
# for x in range(3):
#     stocks_file = f"{dir_name}/{by_end[x][0]}.txt"
#     with open(stocks_file, "r", newline="", encoding="utf-8") as f:
#         row_list = parse_stock_data(f.read())
#     vals_list = [x["Close"] for x in row_list]
#     date_vals = [x["Date"] for x in row_list]
#     portfolio_values = simulate_strategy(vals_list, initial_cash, buy_amount_pln, sell_amount_pln)
#     plot_charts_rsi(by_end[x][0], date_vals, vals_list, portfolio_values)





# ================================== FIND POTENTIAL ===============================================
import requests
# from bs4 import BeautifulSoup
from lxml import html

for x in range(len(by_end)):
    [index_name, end_value, min_value, max_value] = by_end[x]

    if min_value < 0.9*(initial_cash + initial_stock_value):   # skip if strategy failed significantly
        continue
    with open(f"stocks/{index_name}.txt", "r", newline="", encoding="utf-8") as f:
        row_list = parse_stock_data(f.read())
        row_list = row_list[dates_to_parse:]
        vals_list = [x["Close"] for x in row_list]
        date_vals = [x["Date"] for x in row_list]

        rsi_vals = calculate_rsi(vals_list, period=14)
        rsi_vals_last = rsi_vals[-rsi_critical_period:]
        if min(rsi_vals_last) < 30 or max(rsi_vals_last) > 70:
            portfolio_values = simulate_strategy(vals_list, initial_cash, initial_stock_value, buy_amount_pln, sell_amount_pln)

            url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{index_name}"
            headers = { "User-Agent": "Mozilla/5.0" }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            tree = html.fromstring(response.text)
            xpath = '/html/body/div[2]/div[2]/div[1]/div/main/div/div/div[4]/div[3]'
            section = tree.xpath(xpath)
            plain_text = ""
            if section:
                html_section = html.tostring(section[0], encoding='unicode')
                tree = html.fromstring(html_section)
                plain_text = tree.text_content().strip()
                plain_text = plain_text.encode('ascii', 'ignore').decode('ascii')
                plain_text = plain_text.replace("\t", "").replace("\r", " ").replace("\n", "").replace("r/r", "\n")
                plain_text = plain_text.replace("POZYTYWNE", "POZYTYWNE\n").replace("NEGATYWNE", "NEGATYWNE\n")
            plot_charts_rsi_trend_br(by_end[x][0], date_vals, vals_list, portfolio_values, plain_text)


        a = 0


