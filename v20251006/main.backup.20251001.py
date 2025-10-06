import os
from calculate_rsi import calculate_rsi
from functions import parse_stock_data
from plot_charts import plot_charts_rsi_trend_br
from rsi.functions import get_stocks, write_table, save_stock_profit_list
from rsi.get_stock_profit_list import get_stock_profit_list
from values import *
from simulate_strategy import simulate_strategy
import requests
from lxml import html



# ================================== GET DATA ===============================================
if read_from_stooq:
    download_stock_data()
stocks = get_stocks()

# ================================== CALCULATE END PROFIT ===============================================
stock_profit_list = get_stock_profit_list(stocks)
save_stock_profit_list(stock_profit_list)



# ================================== FIND POTENTIAL ===============================================

stock_profit_list = sorted(stock_profit_list, key=lambda x: x[2][-1], reverse=True)  # po End Value
for x in range(len(stock_profit_list)):
    try:
        stock_profit = stock_profit_list[x]
        index_name = stock_profit[0]
        row_list = stock_profit[1]
        portfolio_values = stock_profit[2]
        row_list = row_list[dates_to_parse:]

        vals_list = [x["Close"] for x in row_list]
        date_vals = [x["Date"] for x in row_list]

        rsi_vals = calculate_rsi(vals_list, period=rsi_period)
        rsi_vals_last = rsi_vals[-rsi_critical_period:]
        if min(rsi_vals_last) < 30 or max(rsi_vals_last) > 70 or show_all_charts_not_only_selected_by_rsi:
            portfolio_values = simulate_strategy(vals_list, initial_cash, initial_stock_value, buy_amount_pln, sell_amount_pln)
            portfolio_values = [x - initial_cash for x in portfolio_values]

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

            plot_charts_rsi_trend_br(index_name, date_vals, vals_list, portfolio_values, plain_text)
    except Exception as e:
        print(e)
        print(index_name)
        continue

    a = 0


