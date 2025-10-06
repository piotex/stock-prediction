import math





def is_stock_worth_interest(stock):
    index = stock["index"]
    dates = stock["Date"]       # Time, Open, High, Low
    closes = stock["Close"]
    name = stock["stock_name"]
    tendencies = stock["tendencies"]

    financial_data = stock["financial_data"]
    quarters = financial_data.get('Quarters', [])
    currency = financial_data.get('Waluta', [])
    assets = financial_data.get('Aktywa (tys.)', [])
    equity = financial_data.get('Kapitał własny (tys.)*', [])
    net_sales_revenue = financial_data.get('Przychody netto ze sprzedaży (tys.)', [])
    profit_loss_from_operating_activities = financial_data.get('Zysk (strata) z działal. oper. (tys.)', [])
    gross_profit = financial_data.get('Zysk (strata) brutto (tys.)', [])
    net_profit = financial_data.get('Zysk (strata) netto (tys.)*', [])
    depreciation = financial_data.get('Amortyzacja (tys.)', [])
    EBITDA = financial_data.get('EBITDA (tys.)', [])
    number_of_shares = financial_data.get('Liczba akcji (tys. szt.)', [])
    profit_per_share = financial_data.get('Zysk na akcję (zł)', [])
    book_value_per_share = financial_data.get('Wartość księgowa na akcję (zł)', [])
    auditor_report = financial_data.get('Raport zbadany przez audytora', [])

    if "POZYTYWNE" not in tendencies:
        return False

    if not net_profit[-1] > net_profit[-2]:
        return False

    return True

