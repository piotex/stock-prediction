import os
from datetime import datetime, date
import time
import random
import requests
from typing import Dict, List
from values import *




def get_stock_data(stock_index: str):
    with open(f"stocks/{stock_index}.txt") as f:
        tmp = parse_stock_data(f.read())
        stock = {
            "index": stock_index,
            "Date": [datetime.strptime(x["Date"], '%Y%m%d').date() for x in tmp],
            "Time": [x["Time"] for x in tmp],
            "Open": [x["Open"] for x in tmp],
            "High": [x["High"] for x in tmp],
            "Low": [x["Low"] for x in tmp],
            "Close": [x["Close"] for x in tmp],
        }
        return stock











def parse_stock_data(txt_data: str) -> list:
    lista = txt_data.split()
    ret = []
    for x in lista:
        a = x.split(',')
        ret.append({"Date":a[0], "Time":a[1], "Open":float(a[2]), "High":float(a[3]), "Low":float(a[4]), "Close":float(a[5])})
    return ret




def get_stocks() -> Dict[str, Dict]:
    dir_name = "stocks"
    stocks = {}
    stocks_files = [f"{dir_name}/{x}" for x in os.listdir(dir_name)]
    for stocks_file in stocks_files:
        with open(stocks_file, "r", newline="", encoding="utf-8") as f:
            stock_idx = stocks_file.split("/")[-1].split(".")[0]
            stocks[stock_idx] = parse_stock_data(f.read())
    return stocks


def write_table(f, title, rows):
    f.write(title + "\n")
    f.write(f"{'Index':<10} {'End Value':>15} {'Min':>15} {'Max':>15}\n")
    f.write("-" * 60 + "\n")

    for stock, stock_data, portfolio_values in rows:
        end_val = portfolio_values[-1]
        min_val = min(portfolio_values)
        max_val = max(portfolio_values)

        end_str = f"{end_val:,.2f}".replace(",", " ")
        min_str = f"{min_val:,.2f}".replace(",", " ")
        max_str = f"{max_val:,.2f}".replace(",", " ")

        f.write(
            f"{stock:<10} {end_str:>15} {min_str:>15} {max_str:>15}\n"
        )
    f.write("\n\n")



def save_stock_profit_list(stock_profit_list):
    by_end = sorted(stock_profit_list, key=lambda x: x[2][-1], reverse=True)  # po End Value
    by_min = sorted(stock_profit_list, key=lambda x: min(x[2]), reverse=True)  # po Min
    by_max = sorted(stock_profit_list, key=lambda x: max(x[2]), reverse=True)  # po Max

    by_end = by_end[:rows_to_show_in_wyniki]
    by_min = by_min[:rows_to_show_in_wyniki]
    by_max = by_max[:rows_to_show_in_wyniki]

    with open("wyniki.txt", "w", encoding="utf-8") as f:
        write_table(f, "==== Posortowane po: End Value ====", by_end)
        write_table(f, "==== Posortowane po: Max ====", by_max)
        write_table(f, "==== Posortowane po: Min ====", by_min)
