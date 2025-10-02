import os
import sys
import time
from rsi.download_data import download_stock_data, get_stock_name_and_tendences, get_Skonsolidowany_quarterly_reports, \
    get_Jednostkowy_quarterly_reports
from rsi.functions import get_stock_data
from rsi.plot_charts import print_stock_data
from values import *
import random
import json
from datetime import datetime
import traceback


if clean_all_folders:
    for file in os.listdir("stocks"):
        os.remove(f"stocks/{file}")
    for file in os.listdir("wyniki"):
        os.remove(f"wyniki/{file}")


# ================================== GET DATA ===============================================
if read_from_stooq:
    download_stock_data()
stock_idx_list = [x.split('.')[0] for x in os.listdir("stocks")]
stock_idx_list.sort()



for i, stock_idx in enumerate(stock_idx_list):
    try:
        if read_from_bizradar_and_bankier:
            if os.path.exists(f"wyniki/{stock_idx}.txt"):
                os.remove(f"wyniki/{stock_idx}.txt")

            print(f" {i+1} / {len(stock_idx_list)}  -  {stock_idx}")
            stock_data = get_stock_data(stock_idx)          # {index, Date, Time, Open, High, Low, Close}
            stock_name, tendencies = get_stock_name_and_tendences(stock_data["index"])

            quarterly_reports = {}
            try:
                quarterly_reports = get_Skonsolidowany_quarterly_reports(stock_name)
            except:
                quarterly_reports['Quarters'] = [""]
            if "202" not in quarterly_reports['Quarters'][-1]:
                quarterly_reports = get_Jednostkowy_quarterly_reports(stock_name)



            zysk_netto = quarterly_reports['Zysk (strata) netto (tys.)*']
            if not zysk_netto[-1] > zysk_netto[-2]:
                continue
            if not "EBITDA (tys.)" in quarterly_reports:
                ebitda = quarterly_reports['EBITDA (tys.)']
                if not ebitda[-1] > ebitda[-2]:
                    continue
            if not "Przychody netto ze sprzedaży (tys.)" in quarterly_reports:
                przychod_netto = quarterly_reports['Przychody netto ze sprzedaży (tys.)']
                if not przychod_netto[-1] > przychod_netto[-2]:
                    continue

            time.sleep(random.randint(1, 2))
            with open(f"wyniki/{stock_idx}.txt", "w") as file:
                file.write(stock_name)

    except Exception as e:
        print(f"=========================== ERROR dla: {stock_idx}")
        traceback.print_exc(file=sys.stdout)
        print(e)
        continue


if print_results:
    list_to_process = os.listdir("wyniki")
    for i, file in enumerate(list_to_process):
        stock_data = get_stock_data(file.split('.')[0])         # {index, Date, Time, Open, High, Low, Close}
        stock_name, tendencies = get_stock_name_and_tendences(stock_data["index"])

        quarterly_reports = get_Skonsolidowany_quarterly_reports(stock_name)
        if "202" not in quarterly_reports['Quarters']:
            quarterly_reports = get_Jednostkowy_quarterly_reports(stock_name)

        print(f" {i + 1} / {len(list_to_process)}  -  {stock_name}")
        print_stock_data(stock_name, stock_data["Date"], stock_data["Close"], tendencies, quarterly_reports)

        os.remove(f"wyniki/{file}")

