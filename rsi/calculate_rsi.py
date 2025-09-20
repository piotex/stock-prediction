def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        raise ValueError("Za mało danych do obliczenia RSI")

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    gains = [max(delta, 0) for delta in deltas]
    losses = [abs(min(delta, 0)) for delta in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsis = [None] * (period)

    if avg_loss == 0:
        rs = float('inf')
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    rsis.append(rsi)

    for i in range(period, len(deltas)):
        gain = gains[i]
        loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rs = float('inf')
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsis.append(rsi)

    return rsis