import datetime
import json

import requests


def url_generator(stock_index: str, interval: str, yyyy_mm_dd: str) -> str:
    return f"https://stooq.pl/q/a2/d/?s={stock_index}&i={interval}&f={yyyy_mm_dd}"


def parse_stock_data(txt_data: str) -> list:
    lista = txt_data.split()
    ret = []
    for x in lista:
        a = x.split(',')
        ret.append({"Date": f'{a[0][0:4]}-{a[0][4:6]}-{a[0][6:8]}', "Time": a[1], "Open": float(a[2]),
                    "High": float(a[3]), "Low": float(a[4]), "Close": float(a[5])})
    return ret


def print_number(liczba):
    return "{:.2f}".format(liczba)


def get_data_from_stock(stock_index, interval):
    now = datetime.datetime.now()
    yyyy_mm_dd = f"{now.year:04d}{now.month:02d}{now.day:02d}"
    url = url_generator(stock_index, interval, yyyy_mm_dd)

    resp = requests.get(url)
    ret = parse_stock_data(resp.text)
    return ret


def save_data_to_json(data):
    with open('files/data.json', 'w') as json_file:
        json.dump(data, json_file)


def get_data_from_json():
    with open('files/data.json', 'r') as json_file:
        data = json.load(json_file)
        return data
