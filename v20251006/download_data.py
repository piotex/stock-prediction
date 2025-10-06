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
        time.sleep(random.uniform(1, 2))
        resp = requests.get(f"https://stooq.pl/q/a2/d/?s={index}&i={interval}&f={yyyy_mm_dd}")
        with open(f"{stooq_dir}/{index}.txt", "w", newline="", encoding="utf-8") as f:
            f.writelines(resp.text)
        print(f"Downloaded: {index}   ||   {i+1}/{len(indexes)}")



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




# =================================================================================================
def download_bankier_financial_data():
    pass




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
        a = 0

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


def get_Skonsolidowany_quarterly_reports(stock_name) -> Dict[str, Any]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    url1 = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/1"
    response1 = requests.get(url1, headers=headers)
    response1.raise_for_status()
    resp_text = response1.text
    df1 = _parse_financial_table(resp_text)

    url2 = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/2"
    response2 = requests.get(url2, headers=headers)
    response2.raise_for_status()
    resp_text2 = response2.text
    df2 = _parse_financial_table(resp_text2)

    res_dict = {}
    for res in df1:
        res_dict[res] = df2[res] + df1[res]
        for i in range(len(res_dict[res])):
            if "." in res_dict[res][i]:
                res_dict[res][i] = float(res_dict[res][i])
                continue
            try:
                res_dict[res][i] = int(res_dict[res][i])
            except:
                continue

    test_list = [len(res_dict[key]) for key in res_dict]

    for i in range(len(test_list)-1):
        if test_list[i] != test_list[i+1]:
            raise Exception(f"Wrong numer of columns for: {stock_name}")
    return res_dict

def get_Jednostkowy_quarterly_reports(stock_name) -> Dict[str, Any]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    url1 = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/jednostkowy/kwartalny/standardowy/1"
    response1 = requests.get(url1, headers=headers)
    response1.raise_for_status()
    resp_text = response1.text
    df1 = _parse_financial_table(resp_text)

    url2 = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/jednostkowy/kwartalny/standardowy/2"
    response2 = requests.get(url2, headers=headers)
    response2.raise_for_status()
    resp_text2 = response2.text
    df2 = _parse_financial_table(resp_text2)

    res_dict = {}
    for res in df1:
        res_dict[res] = df2[res] + df1[res]
        for i in range(len(res_dict[res])):
            if "." in res_dict[res][i]:
                res_dict[res][i] = float(res_dict[res][i])
                continue
            try:
                res_dict[res][i] = int(res_dict[res][i])
            except:
                continue

    test_list = [len(res_dict[key]) for key in res_dict]

    for i in range(len(test_list)-1):
        if test_list[i] != test_list[i+1]:
            raise Exception(f"Wrong numer of columns for: {stock_name}")
    return res_dict

# def get_quarterly_reports(stock_name) -> Dict[str, Any]:
#     url = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     response_text = response.text
#     # tables = pd.read_html(response_text, match='Przychody netto ze sprzedaży', flavor='lxml')
#     tables = pd.read_html(
#         response_text,
#         match='Przychody netto ze sprzedaży',
#         flavor='lxml',
#         thousands=r'[\s\xa0]',
#         decimal=','
#     )
#     aaaaa = tables[0].to_string().replace('\xa0', '').replace(',', '.')
#     df = pd.read_csv(io.StringIO(aaaaa), sep='\s\s+', engine='python', index_col=0)
#     df_transposed = df.set_index(df.columns[0])
#
#     nowy_wiersz_df = pd.DataFrame(
#         [df_transposed.columns.tolist()],
#         columns=df_transposed.columns,
#         index=['Quarters']
#     )
#     df_transposed = pd.concat([nowy_wiersz_df, df_transposed])
#
#     tmp = df_transposed.T.to_dict(orient='list')
#     result = {}
#     for key, val in tmp.items():
#         if "." in val[0]:
#             result[key] = [float(v) for v in val]
#             continue
#         if val[0].isdigit():
#             result[key] = [int(v) for v in val]
#             continue
#         result[key] = val
#
#     url = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/2"
#
#     return result






# def get_quarterly_reports(stock_name):
#     url = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_name}/wyniki-finansowe"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     full_tree = html.fromstring(response.text)
#
#     # --- Pobieranie Raportu ---
#     xpath_tendency = '/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]'
#     section_tendency = full_tree.xpath(xpath_tendency)
#     if section_tendency:
#         plain_text = section_tendency[0].text_content().strip()
#
#         A = 0



















