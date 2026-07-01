from ta.momentum import RSIIndicator


def get_rsi(data):
    rsi = RSIIndicator(close=data["Close"], window=14).rsi()
    return float(rsi.iloc[-1])