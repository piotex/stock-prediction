from calculate_rsi import calculate_rsi
import math

buy_threshold = 30
sell_threshold = 70


def simulate_strategy(vals_list, initial_cash, initial_stock_value, buy_amount_pln, sell_amount_pln):
    rsi_vals = calculate_rsi(vals_list, period=14)
    cash_pln = initial_cash
    initial_stock_numer = int(initial_stock_value // vals_list[0])

    buy_vals = []
    sell_vals = []
    for val in rsi_vals:
        if val is None:
            buy_vals.append(2)
            sell_vals.append(0)
            continue

        if val < buy_threshold:
            buy_vals.append(1)
        else:
            buy_vals.append(0)

        if val > sell_threshold:
            sell_vals.append(1)
        else:
            sell_vals.append(0)

    portfolio_values = []

    for price, buy, sell in zip(vals_list, buy_vals, sell_vals):
        # BUY – kupujemy całkowitą liczbę jednostek za 1500 PLN (jeśli mamy środki)
        if buy == 1 and cash_pln >= price:
            units_to_buy = int(buy_amount_pln // price)
            cost = units_to_buy * price
            if units_to_buy > 0 and cash_pln >= cost:
                initial_stock_numer += units_to_buy
                cash_pln -= cost

        # SELL – sprzedajemy całkowitą liczbę jednostek o wartości 1500 PLN
        if sell == 1 and initial_stock_numer > 0:
            units_to_sell = int(sell_amount_pln // price)
            if units_to_sell > initial_stock_numer:
                units_to_sell = initial_stock_numer  # nie sprzedamy więcej niż mamy
            if units_to_sell > 0:
                initial_stock_numer -= units_to_sell
                cash_pln += units_to_sell * price

        # wartość portfela w danym momencie (PLN + USD w PLN)
        portfolio_value = cash_pln + initial_stock_numer * price
        portfolio_values.append(portfolio_value)

    return portfolio_values
