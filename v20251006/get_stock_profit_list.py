from simulate_strategy import simulate_strategy
from values import *

def get_stock_profit_list(stocks):
    stock_profit_list = []
    for stock, stock_data in stocks.items():
        row_list = stock_data[dates_to_parse:]
        vals_list = [x["Close"] for x in row_list]

        portfolio_values = simulate_strategy(vals_list,
                                             initial_cash,
                                             initial_stock_value,
                                             buy_amount_pln,
                                             sell_amount_pln)

        portfolio_values = [x - initial_cash for x in portfolio_values]

        stock_profit_list.append([
            stock,
            stock_data,
            portfolio_values
        ])
    return stock_profit_list