import pandas as pd

high_threshold = 80
low_threshold = 20


def calculate_rsi(stooq_vals, period=14):
    stooq_vals = pd.Series(stooq_vals)
    # Oblicz różnice między kolejnymi cenami
    delta = stooq_vals.diff()

    # Oddziel zyski i straty
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    # Oblicz RS (Relative Strength)
    rs = gain / loss

    # Oblicz RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi.tolist()


def get_rsi_operations(stooq_vals, period):     # start, end, operation -> "buy" "sell"
    rsi_values = calculate_rsi(stooq_vals, period)
    operations = []
    start_sell_i = -1
    start_buy_i = -1
    for i in range(0, len(rsi_values)):
        rsi = rsi_values[i]
        if rsi > high_threshold and start_sell_i == -1:
            start_sell_i = i
        if rsi < high_threshold and start_sell_i != -1:
            operations.append([start_sell_i, i, "sell"])
            start_sell_i = -1

        if rsi < low_threshold and start_buy_i == -1:
            start_buy_i = i
        if rsi > low_threshold and start_buy_i != -1:
            operations.append([start_buy_i, i, "buy"])
            start_buy_i = -1
    return operations


def get_rsi_histogram_operations(stooq_vals):   # +1 buy | -1 sell
    histogram = [0 for x in stooq_vals]
    for period in range(3,32):
        rsi_values = calculate_rsi(stooq_vals, period)
        for i, rsi in enumerate(rsi_values):
            if rsi > high_threshold:
                histogram[i] += -1
            if rsi < low_threshold:
                histogram[i] += 1
    return histogram

