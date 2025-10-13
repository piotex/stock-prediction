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


# ================================== FIND STOCKS WORTH INVESTMENT ===============================================
stocks_worth_interest = {}
for index, data in valid_data.items():
    if not is_stock_worth_interest(data):
        continue
    stocks_worth_interest[index] = data


# ================================== TMP ===============================================
tmp_vals = []
for key, value in valid_data.items():
    tmp = determine_recommended_purchase_price(value)
    recommended_purchase_price = tmp['recommended_purchase_price']
    latest_close_price = tmp['latest_close_price']
    valid_data[key]["recommended_purchase_price"] = recommended_purchase_price
    tmp_vals.append([key, latest_close_price, recommended_purchase_price, (recommended_purchase_price-latest_close_price)/latest_close_price])

sorted_ressss = sorted(tmp_vals, key=lambda x: x[-1], reverse=True)
for item in sorted_ressss:
    data = valid_data[item[0]]
    print_stock_data(
        stock_name=data["stock_name"],
        dates=data["Date"],
        prices=data["Close"],
        tendencies=data["tendencies"],
        indicators=data["indicators"],
        quarterly_data=data["financial_data"],
        recommended_purchase_price=data["recommended_purchase_price"],
    )


# ================================== PRINT STOCKS WORTH INVESTMENT ===============================================
if print_stocks_worth_interest:
    print(f"stocks_worth_interest (count): {len(stocks_worth_interest)}")
    for index, data in stocks_worth_interest.items():
        print(f"{stocks_worth_interest[index]["stock_name"]}")

if print_stock_data_results:
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













#