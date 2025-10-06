from typing import Dict, List, Tuple, Any
import os
import datetime
import time
import random
import requests
from values import *
from lxml import html
import pandas as pd
import io
import re
from io import StringIO
import json

# =================================================================================================
def download_stock_data():
    stooq_dir = "00-stooq-stocks-values"
    for f in os.listdir(stooq_dir):
        os.remove(os.path.join(stooq_dir, f))

    indexes_dir = "indeksy"
    indexes_files = [f"{os.path.join(indexes_dir, x)}" for x in os.listdir(indexes_dir)]
    indexes = [
        x.strip()
        for file in indexes_files
        for x in open(file).readlines()
    ]

    yyyy_mm_dd = f"{datetime.datetime.now().year:04d}{datetime.datetime.now().month:02d}{datetime.datetime.now().day:02d}"
    for i, index in enumerate(indexes):
        try:
            time.sleep(random.uniform(1, 2))
            resp = requests.get(f"https://stooq.pl/q/a2/d/?s={index}&i={interval}&f={yyyy_mm_dd}")
            with open(f"{stooq_dir}/{index}.txt", "w", newline="", encoding="utf-8") as f:
                f.writelines(resp.text)
            print(f"Downloaded: {index}   ||   {i+1}/{len(indexes)}")
        except Exception as e:
            print(f"Error: {index}   ||   {i+1}/{len(indexes)} - {e}")


# =================================================================================================
def _get_stock_name_and_tendences(index_name) -> Tuple[str, str]:
    url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{index_name}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    full_tree = html.fromstring(response.text)
    tendencies = ""
    stock_name = ""

    # --- Pobieranie Tendencji ---
    xpath_tendency = '/html/body/div[2]/div[2]/div[1]/div/main/div/div/div[4]/div[3]'
    section_tendency = full_tree.xpath(xpath_tendency)
    if section_tendency:
        plain_text = section_tendency[0].text_content().strip()
        plain_text = plain_text.encode('ascii', 'ignore').decode('ascii')
        plain_text = plain_text.replace("\t", "").replace("\r", " ").replace("\n", "").replace('r/r', 'r/r\n')
        plain_text = plain_text.replace("POZYTYWNE", "POZYTYWNE\n").replace("NEGATYWNE", "NEGATYWNE\n")
        tendencies = plain_text

    # --- Pobieranie Nazwy Akcji (Z całego drzewa) ---
    xpath_name = "//h1"
    name_elements = full_tree.xpath(xpath_name)
    if name_elements:
        stock_text = name_elements[0].text_content().strip()
        if "(" in stock_text:
            stock_name = stock_text.split('(')[1].split(')')[0]
        else:
            stock_name = index_name

    return stock_name, tendencies

def download_bizradar_tendencies():
    stooq_dir = "01-biznesradar-tendencies"
    for f in os.listdir(stooq_dir):
        os.remove(os.path.join(stooq_dir, f))

    indexes_dir = "00-stooq-stocks-values"
    indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
    for i, index in enumerate(indexes):
        try:
            time.sleep(random.uniform(1, 2))
            stock_name, tendencies = _get_stock_name_and_tendences(index)
            with open(f"{stooq_dir}/{index}.json", "w", newline="", encoding="utf-8") as file:
                data_obj = {
                    "stock_index": index,
                    "stock_name": stock_name,
                    "tendencies": tendencies,
                }
                json.dump(data_obj, file, indent=4, ensure_ascii=False)
            print(f"Downloaded: {index}   ||   {i+1}/{len(indexes)}")
        except Exception as e:
            print(f"Error: {index}   ||   {i+1}/{len(indexes)} - {e}")



# =================================================================================================
def _parse_financial_table(response_text: str) -> dict[str, List[str]]:
    tables = pd.read_html(
        StringIO(response_text),
        match='Aktywa',
        flavor='lxml',
        thousands=r'[\s\xa0]',
        decimal=','
    )
    aaaaa = (tables[0].to_string()
             .replace('\xa0', '')
             .replace(',', '.')
             .replace("\n"," \n")
             .replace("Unnamed: 0", "Unnamed: 0 ")
             + " ")

    wzorzec = r'(\d{4})(\s?)(I{1,3})'
    zamiana = r'\1  \3'
    aaaaa = re.sub(wzorzec, zamiana, aaaaa)

    res_list = []
    for line in aaaaa.split('\n'):
        valll = []
        i = 0
        while i < len(line)-1:
            while(line[i] == " "):
                i += 1
            valll.append("")
            while(line[i] != " " or line[i+1] != " "):
                valll[-1] += line[i]
                i += 1
                if i == len(line) - 1:
                    break
            i+=1
        if line[-1] != " ":
            valll[-1] += line[-1]
        res_list.append(valll)

    for res in res_list:
        res.pop(0)
    res_list[0].insert(0, "Quarters")

    res_dict = {}
    for res in res_list:
        res_dict[res[0]] = res[1:]

    test_list = [len(res_dict[key]) for key in res_dict]
    for i in range(len(test_list)-1):
        if test_list[i] != test_list[i+1]:
            aaaa_ok = False

    return res_dict

def _clean_and_convert_data(df1: Dict, df2: Dict, stock_name: str) -> Dict[str, Any]:
    res_dict = {}
    for key in df1:
        combined_list = df2.get(key, []) + df1[key]
        converted_list = []
        for item in combined_list:
            item = item.replace(",", "")
            if not item:
                converted_list.append(None)
                continue

            try:
                if "." in item:
                    converted_list.append(float(item))
                else:
                    converted_list.append(int(item))
            except ValueError:
                converted_list.append(item)

        res_dict[key] = converted_list

    lengths = [len(res_dict[key]) for key in res_dict]
    if lengths and any(l != lengths[0] for l in lengths):
        raise Exception(f"Błędna liczba kwartałów w kolumnach dla: {stock_name}")
    return res_dict

def _get_quarterly_reports(stock_name: str, report_type: str) -> Dict[str, Any]:
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    data_frames = {}
    MAX_RETRIES = 3
    RETRY_DELAY = 15

    for page_num in [1, 2]:
        url = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/{report_type}/kwartalny/standardowy/{page_num}"
        attempts = 0
        while attempts < MAX_RETRIES:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if 400 <= response.status_code <= 499:
                response.raise_for_status()
            if 500 <= response.status_code <= 599:
                attempts += 1
                time.sleep(RETRY_DELAY)
                continue
            break
        if attempts == MAX_RETRIES:
            raise requests.exceptions.RequestException(f"[Downloading Error - Bankier - Financial Report] Failed to retrieve data for {stock_name} after {MAX_RETRIES} attempts.")

        resp_text = response.text
        data_frames[page_num] = _parse_financial_table(resp_text)
    return _clean_and_convert_data(
        df1=data_frames[1],
        df2=data_frames[2],
        stock_name=stock_name
    )

def download_bankier_financial_data():
    stooq_dir = "02-bankier-financial-data"
    for f in os.listdir(stooq_dir):
        os.remove(os.path.join(stooq_dir, f))

    sleep_times = [3, 10]
    indexes_dir = "01-biznesradar-tendencies"
    indexes = [f"{x.split('.')[0]}" for x in os.listdir(indexes_dir)]
    for i, index in enumerate(indexes):
        try:
            stock_name = json.load(open(f"{indexes_dir}/{index}.json", "r", encoding="utf-8"))["stock_name"]
            try:
                time.sleep(random.uniform(sleep_times[0], sleep_times[1]))
                quarterly_reports = _get_quarterly_reports(stock_name, "skonsolidowany")
            except:
                time.sleep(random.uniform(sleep_times[0], sleep_times[1]))
                quarterly_reports = _get_quarterly_reports(stock_name, "jednostkowy")

            with open(f"{stooq_dir}/{index}.json", "w", newline="", encoding="utf-8") as file:
                json.dump(quarterly_reports, file, indent=4, ensure_ascii=False )
            print(f"Downloaded: {index}   ||   {i + 1}/{len(indexes)}")
        except Exception as e:
            print(f"Error: {index}   ||   {i+1}/{len(indexes)} - {e}")


# =================================================================================================






