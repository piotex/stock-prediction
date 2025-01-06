import requests
import time
import random

with open('../files/indexes.txt', 'r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]
res_idx = []
for index in lines:
    # if index == "3RGAMES":
    #     break
    url = f"https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={index}"
    response = requests.get(url)
    if response.status_code == 200:
        selector = '<span class="profilTicker">'
        tmp = response.text
        index = tmp.find(selector) + len(selector)
        start = False
        res = ""
        for i in range(index, len(tmp)):
            if tmp[i] == ")":
                break
            if tmp[i] == "(":
                start = True
                continue
            if start:
                res += tmp[i]
        res_idx.append(f"{res}\n")
        with open('../files/indexes_conv.txt', 'w', encoding='utf-8') as file:
            file.writelines(res_idx)
        time.sleep(random.randint(1, 3))
    else:
        print(f"Error: {response.status_code}")
