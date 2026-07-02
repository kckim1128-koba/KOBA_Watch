import yfinance as yf


def get_latest_price_info(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="3mo")

    if data is None or data.empty or len(data) < 2:
        return None

    close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]
    change = ((close - prev_close) / prev_close) * 100

    return {
        "symbol": symbol,
        "data": data,
        "close": float(close),
        "change": float(change),
    }