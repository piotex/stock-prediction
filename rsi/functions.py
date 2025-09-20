def url_generator(stock_index: str, interval: str, yyyy_mm_dd: str) -> str:
  return f"https://stooq.pl/q/a2/d/?s={stock_index}&i={interval}&f={yyyy_mm_dd}"

def parse_stock_data(txt_data: str) -> list:
    lista = txt_data.split()
    ret = []
    for x in lista:
        a = x.split(',')
        ret.append({"Date":a[0], "Time":a[1], "Open":float(a[2]), "High":float(a[3]), "Low":float(a[4]), "Close":float(a[5])})
    return ret