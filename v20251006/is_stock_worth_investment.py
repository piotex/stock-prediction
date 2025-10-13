import math
import re


def get_numeric_value(indicator_list, index=-1):
    if not indicator_list:
        return None
    try:
        raw_string = str(indicator_list[index]).strip()
        if raw_string == '-':
            return None
        raw_value = raw_string.split('~')[0].strip()
        raw_value = raw_value.replace(' ', '').replace(',', '.')
        return float(raw_value)
    except (IndexError, ValueError):
        return None
    except Exception:
        return None


def calculate_change(indicator_list, index=-1, change_type='r/r'):
    """
    Oblicza zmianę procentową R/R (rok do roku, 4 kwartały wstecz)
    lub Q/Q (kwartał do kwartału, 1 kwartał wstecz)
    na podstawie czystych wartości liczbowych.
    """
    if not indicator_list:
        return None

    step = 0
    if change_type == 'r/r':
        step = 4
    elif change_type == 'k/k':
        step = 1
    else:
        return None

    if abs(index) < step:  # Nie ma wystarczającej liczby danych do porównania
        return None

    current_value = get_numeric_value(indicator_list, index)
    previous_value = get_numeric_value(indicator_list, index - step)  # Cofnięcie o step kwartałów

    if current_value is None or previous_value is None or previous_value == 0:
        return None

    # Obliczanie zmiany procentowej
    change = (current_value - previous_value) / previous_value
    return change


def is_stock_worth_interest(stock):
    # Kryteria Wyceny (Value Investing)
    PE_MAX = 25.0                   # Maksymalny akceptowalny wskaźnik C/Z
    PB_MAX = 3.0                    # Maksymalny akceptowalny wskaźnik C/WK
    PS_MAX = 2.0                    # Maksymalny akceptowalny wskaźnik C/P - Cena / Przychody ze Sprzedaży
    EV_EBITDA_MAX = 10.0            # Maksymalny akceptowalny wskaźnik EV/EBITDA

    # Kryteria Wzrostu i Efektywności (Growth & Efficiency)
    EPS_GROWTH_MIN_RR = 0.10        # Minimalny wymagany wzrost Zysku na Akcję r/r (10%)
    BVS_DECREASE_MAX_RR = -0.05     # Maksymalny akceptowalny spadek Wartości Księgowej na Akcję r/r (-5%)
    EBIT_PER_SHARE_MIN = 0.0        # Minimalna wartość Zysku Operacyjnego na Akcję (dodatni)
    # ====================================================

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
    ev_to_ebitda = indicators.get('EV / EBITDA', [])



    # 1. Analiza Trendu (Tendencies)
    if "POZYTYWNE" not in stock["tendencies"]:
        return False

    # 2. Ciągły wzrost Zysku Netto Q/Q (FINANCIAL DATA)
    net_profit_current = get_numeric_value(net_profit, -1)
    net_profit_previous = get_numeric_value(net_profit, -2) # Q-1
    if not net_profit_current > net_profit_previous:
         return False

    # 2b. Wzrost Zysku na Akcję (EPS) Q/Q (INDICATORS)
    eps_current = get_numeric_value(earnings_per_share, -1)
    eps_previous = get_numeric_value(earnings_per_share, -2) # Q-1
    if not eps_current > eps_previous:
        return False

    # 3. Kryteria Wyceny (Value Investing)

    # P/E (Cena / Zysk)
    pe_ratio = get_numeric_value(price_to_earnings, -1)
    if pe_ratio is not None and pe_ratio > PE_MAX:
        return False

    # P/BV (Cena / Wartość księgowa)
    pb_ratio = get_numeric_value(price_to_book_value, -1)
    if pb_ratio is not None and pb_ratio > PB_MAX:
        return False

    # P/S (Cena / Przychody)
    ps_ratio = get_numeric_value(price_to_sales_revenue, -1)
    if ps_ratio is not None and ps_ratio > PS_MAX:
        return False

    ## Kryteria Wzrostu i Efektywności (Growth & Efficiency)

    # 4. Wzrost Zysku na Akcję (EPS) r/r (rok do roku)
    eps_change_yr = calculate_change(earnings_per_share, -1, change_type='r/r')
    if eps_change_yr is None or eps_change_yr < EPS_GROWTH_MIN_RR:
        return False

    # 5. Stabilna Wartość Księgowa na Akcję (BVS) r/r
    bvs_change_yr = calculate_change(book_value_per_share, -1, change_type='r/r')
    if bvs_change_yr is None or bvs_change_yr < BVS_DECREASE_MAX_RR:
        return False

    # 6. Rentowność: Dodatni i stabilny Zysk Operacyjny (EBIT) - na akcję (EPS)
    ebit_per_share_current = get_numeric_value(operating_profit_per_share, -1)
    if ebit_per_share_current is None or ebit_per_share_current <= EBIT_PER_SHARE_MIN:
        return False

    # 7. Relatywna Wycena (EV/EBITDA)
    ev_ebitda = get_numeric_value(ev_to_ebitda, -1)
    if ev_ebitda is not None and ev_ebitda > EV_EBITDA_MAX:
        return False

    return True