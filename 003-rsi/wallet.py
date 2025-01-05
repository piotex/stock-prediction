from rsi import get_rsi_operations


def get_wallet_values_in_time(stooq_vals, period):
    rsi_operations = get_rsi_operations(stooq_vals, period)

    wallet_money_in_time = []
    wallet_money = 0
    wallet_shares_count = 0
    single_operation_cost = 1000
    transaction_cost = 5

    for i in range(0, len(stooq_vals)):
        stock_val = stooq_vals[i]
        for period_start_end_type in rsi_operations:
            period_start = period_start_end_type[0]
            period_end = period_start_end_type[1]
            operation_type = period_start_end_type[2]

            if period_start <= i <= period_end:
                number_of_stocks = int(single_operation_cost / stock_val)
                if operation_type == "buy":
                    wallet_shares_count += number_of_stocks
                    wallet_money -= number_of_stocks * stock_val
                    wallet_money -= transaction_cost

                if operation_type == "sell":
                    if wallet_shares_count == 0:
                        break
                    if number_of_stocks > wallet_shares_count:  # don't sell shares that doesn't have
                        number_of_stocks = wallet_shares_count
                    wallet_shares_count -= number_of_stocks
                    wallet_money += number_of_stocks * stock_val
                    wallet_money -= transaction_cost
                break
        wallet_money_in_time.append(wallet_money + (wallet_shares_count * stooq_vals[i]))
    return wallet_money_in_time