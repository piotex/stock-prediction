import math

def get_eps_value(indicator_list, index=-1):
    if not indicator_list:
        return None
    try:
        # Format: '0,62r/r +255.15%k/k -4.54%'
        raw_value = str(indicator_list[index]).split('r/r')[0].replace(',', '.')
        return float(raw_value)
    except (IndexError, ValueError):
        return None


def get_change(indicator_list, index=-1, change_type='r/r'):
    """
    Ekstrahuje zmianę r/r (rok do roku) lub k/k (kwartał do kwartału)
    dla wskaźników formatu 'wartość~branża...'. Zwraca None w przypadku braku.
    """
    if not indicator_list:
        return None

    try:
        raw_string = str(indicator_list[index])

        if change_type == 'r/r':
            start_marker = 'r/r '
        elif change_type == 'k/k':
            start_marker = 'k/k '
        else:
            return None

        if start_marker not in raw_string:
            return None

        # Wyszukiwanie zmiany dla Spółki, ignorując zmianę dla branży
        parts = raw_string.split('~')

        # Iteracja po częściach (poza samą wartością) w poszukiwaniu r/r lub k/k
        for part in parts[1:]:
            if start_marker in part:
                # Wyszukaj i wyodrębnij wartość procentową
                start_index = part.find(start_marker) + len(start_marker)
                end_index = part.find('%', start_index)

                if end_index != -1:
                    change_value = part[start_index:end_index].replace(',', '.')
                    return float(change_value) / 100
    except Exception:
        return None

    return None

def get_value(indicator_list, index=-1):
    if not indicator_list:
        return None
    try:
        raw_value = str(indicator_list[index]).split('~')[0].replace(',', '.')
        return float(raw_value)
    except (IndexError, ValueError):
        return None

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

    indicators = stock["indicators"]
    quarters = indicators.get('Quarters', [])
    price = indicators.get('Kurs', [])
    number_of_shares = indicators.get('Liczba akcji', [])
    price_to_sales_revenue = indicators.get('Cena / Przychody ze sprzedaży', [])
    price_to_book_value = indicators.get('Cena / Wartość księgowa', [])
    price_to_graham_book_value = indicators.get('Cena / Wartość księgowa Grahama', [])
    price_to_earnings = indicators.get('Cena / Zysk', [])
    price_to_operating_profit = indicators.get('Cena / Zysk operacyjny', [])
    ev_to_ebit = indicators.get('EV / EBIT', [])
    ev_to_ebitda = indicators.get('EV / EBITDA', [])
    ev_to_sales_revenue = indicators.get('EV / Przychody ze sprzedaży', [])
    enterprise_value_per_share = indicators.get('Enterprise Value na akcję', [])
    sales_revenue_per_share = indicators.get('Przychody ze sprzedaży na akcję', [])
    graham_book_value_per_share = indicators.get('Wartość księgowa Grahama na akcję', [])
    book_value_per_share = indicators.get('Wartość księgowa na akcję', [])
    earnings_per_share = indicators.get('Zysk na akcję', [])
    operating_profit_per_share = indicators.get('Zysk operacyjny na akcję', [])

    if "POZYTYWNE" not in tendencies:
        return False

    if not net_profit[-1] > net_profit[-2]:
        return False

    # 2. Ciągły wzrost zysku netto Q/Q (zachowane)
    eps_current = get_eps_value(earnings_per_share, -1)
    eps_previous = get_eps_value(earnings_per_share, -2)

    # Podstawowy warunek dla zysku netto - wzrost q/q
    if eps_current is None or eps_previous is None or not eps_current > eps_previous:
        return False

    # 3. Dodatkowe warunki fundamentalne (na podstawie wskaźników)
    ## Kryteria Wyceny (Value Investing)

    # P/E (Cena / Zysk): Atrakcyjnie, jeśli poniżej progu (np. 15, ale to zależy od branży)
    pe_ratio = get_value(price_to_earnings, -1)
    if pe_ratio is not None and pe_ratio > 25.0:  # Wskaźnik PE za wysoki (arbitralny próg)
        return False

    # P/BV (Cena / Wartość księgowa): Atrakcyjnie, jeśli poniżej 3.0 lub blisko 1.0
    pb_ratio = get_value(price_to_book_value, -1)
    if pb_ratio is not None and pb_ratio > 3.0:  # Akcje drogie względem kapitału
        return False

    # P/S (Cena / Przychody): Poniżej 1.0 to świetnie, ale dla większości branż poniżej 3.0.
    ps_ratio = get_value(price_to_sales_revenue, -1)
    if ps_ratio is not None and ps_ratio > 2.0:  # Akcje drogie względem przychodów
        return False

    ## Kryteria Wzrostu i Efektywności (Growth & Efficiency)
    # 4. Wzrost Zysku na Akcję (EPS) r/r (rok do roku) - dynamiczny wzrost
    eps_change_yr = get_change(earnings_per_share, -1, change_type='r/r')
    if eps_change_yr is not None and eps_change_yr < 0.10:  # Wzrost EPS r/r poniżej 10%
        return False

    # 5. Stabilna Wartość Księgowa na Akcję (BVS) r/r - kapitał nie maleje
    bvs_change_yr = get_change(book_value_per_share, -1, change_type='r/r')
    if bvs_change_yr is not None and bvs_change_yr < -0.05:  # Spadek BVS r/r o więcej niż 5%
        return False

    # 6. Rentowność: Dodatni i stabilny Zysk Operacyjny (EBIT)
    ebit_current = get_eps_value(operating_profit_per_share, -1)  # uzywam eps_value do ekstrakcji
    if ebit_current is not None and ebit_current <= 0:  # Zysk operacyjny na akcję musi być dodatni
        return False

    # 7. Relatywna Wycena (EV/EBITDA) - Wycena atrakcyjna względem gotówki operacyjnej
    ev_ebitda = get_value(ev_to_ebitda, -1)
    if ev_ebitda is not None and ev_ebitda > 10.0:  # Wskaźnik EV/EBITDA za wysoki
        return False

    return True

