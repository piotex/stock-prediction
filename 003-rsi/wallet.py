from rsi import get_rsi_operations


def get_wallet_values_in_time(stooq_vals, period, initial_capital=10000, percent_buy=0.1, percent_sell=0.25):
    rsi_operations = get_rsi_operations(stooq_vals, period)

    wallet_money_in_time = []
    wallet_money = initial_capital
    wallet_shares_count = 0
    # single_operation_cost = 1000
    transaction_cost = 5

    for i in range(0, len(stooq_vals)):
        stock_val = stooq_vals[i]
        for period_start_end_type in rsi_operations:
            period_start = period_start_end_type[0]
            period_end = period_start_end_type[1]
            operation_type = period_start_end_type[2]

            if period_start <= i <= period_end:
                if operation_type == "buy":
                    number_of_stocks = int(wallet_money*percent_buy / stock_val)
                    wallet_shares_count += number_of_stocks
                    wallet_money -= number_of_stocks * stock_val
                    wallet_money -= transaction_cost

                if operation_type == "sell":
                    number_of_stocks = int(wallet_shares_count*percent_sell)
                    if wallet_shares_count == 0:
                        break
                    wallet_shares_count -= number_of_stocks
                    wallet_money += number_of_stocks * stock_val
                    wallet_money -= transaction_cost
                break
        wallet_money_in_time.append(wallet_money + (wallet_shares_count * stooq_vals[i]))
    # print(f"End number of shares: {wallet_shares_count}")
    # print(f"End wallet money:     {wallet_money}")

    return wallet_money_in_time