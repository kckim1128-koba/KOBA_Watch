import yfinance as yf


def get_latest_price_info(symbol):
    """
    Yahoo Finance에서 현재가와 전일 대비 등락률을 조회
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")

    if hist.empty or len(hist) < 2:
        return {
            "symbol": symbol,
            "price": None,
            "change_percent": None,
        }

    prev_close = hist["Close"].iloc[-2]
    latest_close = hist["Close"].iloc[-1]

    change_percent = ((latest_close - prev_close) / prev_close) * 100

    return {
        "symbol": symbol,
        "price": round(latest_close, 2),
        "change_percent": round(change_percent, 2),
    }