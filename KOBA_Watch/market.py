import yfinance as yf


def get_price_data(symbol, period="3mo"):
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period)


def get_latest_price_info(symbol):
    data = get_price_data(symbol, period="3mo")

    if data.empty or len(data) < 2:
        return None

    close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]
    change = (close - prev_close) / prev_close * 100

    return {
        "data": data,
        "close": float(close),
        "change": float(change),
    }