import json
import os
from v20251006.download_data import download_stock_data, download_bizradar_tendencies, download_bankier_financial_data, \
    download_bizradar_indicators
from v20251006.functions import get_stock_data, measure_execution_time
from v20251006.get_price_when_to_buy import determine_recommended_purchase_price
from v20251006.is_stock_worth_investment import is_stock_worth_interest
from v20251006.plot_charts import print_stock_data
from values import *
import traceback
from tabulate import tabulate
import json
from typing import Dict, Any # Dodaj te importy, jeśli ich brakuje


if clean_all_folders:
    folders_to_clean = [
        "00-stooq-stocks-values",
        "01-biznesradar-tendencies",
        "01-biznesradar-indicators",
        "02-bankier-financial-data",
    ]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)
        os.makedirs(folder, exist_ok=True)


# ================================== GET DATA ===============================================
if download_from_stooq:
    measure_execution_time(download_stock_data, "download_stock_data")

if download_from_bizradar_tendencies:
    measure_execution_time(download_bizradar_tendencies, "download_bizradar_tendencies")

if download_from_bizradar_indicators:
    measure_execution_time(download_bizradar_indicators, "download_bizradar_indicators")

if download_from_bankier_financial_data:
    measure_execution_time(download_bankier_financial_data, "download_bankier_financial_data")

stocks_data = {}
indexes_dir = "00-stooq-stocks-values"
indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
for index in indexes:
    try:
        data = get_stock_data(index)                                                    # {index, Date, Time, Open, High, Low, Close}
        stocks_data[index] = data
    except Exception as e:
        print(f"{index} - Exception get_stock_data: {e}")
        traceback.print_exc()

indexes_dir = "01-biznesradar-tendencies"
indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
for index in indexes:
    try:
        data = json.load(open(f"{indexes_dir}/{index}.json", "r", encoding="utf-8"))    # {stock_name, stock_index, tendencies}
        for key, value in data.items():
            stocks_data[index][key] = value
    except Exception as e:
        print(f"{index} - Exception tendencies: {e}")
        traceback.print_exc()

indexes_dir = "01-biznesradar-indicators"
indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
for index in indexes:
    try:
        data = json.load(open(f"{indexes_dir}/{index}.json", "r", encoding="utf-8"))    # {...}
        stocks_data[index]["indicators"] = data
    except Exception as e:
        print(f"{index} - Exception indicators: {e}")
        traceback.print_exc()

indexes_dir = "02-bankier-financial-data"
indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
for index in indexes:
    try:
        data = json.load(open(f"{indexes_dir}/{index}.json", "r", encoding="utf-8"))    # {...}
        stocks_data[index]["financial_data"] = data
    except Exception as e:
        print(f"{index} - Exception financial-data: {e}")
        traceback.print_exc()

# ================================== CHECK IF DATA IS CORRECT ===============================================
valid_data = {}
for key, value in stocks_data.items():
    if "stock_name" not in value:
        continue
    if "Date" not in value:
        continue
    if "Close" not in value:
        continue
    if "tendencies" not in value:
        continue
    if "indicators" not in value:
        continue
    if "financial_data" not in value:
        continue
    valid_data[key] = value


# ================================== CALCULATE RECOMMENDED PURCHASE PRICE ===============================================
for key, value in valid_data.items():
    analysis_result = determine_recommended_purchase_price(value)
    valid_data[key]["recommended_purchase_price"] = analysis_result['recommended_purchase_price']
    valid_data[key]["latest_close_price"] = analysis_result['latest_close_price']


# ================================== FIND STOCKS WORTH INVESTMENT ===============================================
stocks_worth_interest = {}
for index, data in valid_data.items():
    # index = "MBK"
    # data = valid_data[index]
    if not is_stock_worth_interest(data):
        continue
    stocks_worth_interest[index] = data


# ================================== PRINT STOCKS WORTH INVESTMENT ===============================================
if print_in_console_stocks_worth_interest:
    analysis_data_with_potential = []

    for index, data in stocks_worth_interest.items():
        rec_price = data.get("recommended_purchase_price", 0.0)
        close_price = data.get("latest_close_price", data["Close"][-1] if data.get("Close") else 0.0)
        potential_value = (rec_price / close_price - 1) * 100
        row = [
            data.get("stock_name", index),
            f'{close_price:.2f}',
            f'{rec_price:.2f}',
            f'{potential_value:.1f}%',  # Wartość sformatowana do wyświetlenia
            potential_value             # Wartość liczbowa do sortowania
        ]
        analysis_data_with_potential.append(row)

    sorted_data = sorted(analysis_data_with_potential, key=lambda x: x[4], reverse=True)
    analysis_results_list = [row[:-1] for row in sorted_data]

    headers = ["Spółka", "Cena Rynkowa", "Zalecana Cena Zakupu", "Potencjał Zysku"]
    print(tabulate(analysis_results_list, headers=headers, tablefmt="fancy_grid", numalign="right"))


if print_chart_stock_data_results:
    for index, data in stocks_worth_interest.items():
        print_stock_data(
            stock_name                  = data["stock_name"],
            dates                       = data["Date"],
            prices                      = data["Close"],
            tendencies                  = data["tendencies"],
            indicators                  = data["indicators"],
            quarterly_data              = data["financial_data"],
            recommended_purchase_price  =data["recommended_purchase_price"],
        )








