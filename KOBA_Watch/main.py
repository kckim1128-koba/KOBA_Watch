import yfinance as yf

stocks = {
    "SNXX": 100,
    "MUU": 1500,
    "SOXL": 400,
}

print("=" * 40)
print("📈 KOBA Watch")
print("=" * 40)

for symbol, target_price in stocks.items():
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")

    today = data.iloc[-1]
    yesterday = data.iloc[-2]

    close = today["Close"]
    change = (close - yesterday["Close"]) / yesterday["Close"] * 100
    target_gap = (target_price - close) / close * 100

    print(f"종목 : {symbol}")
    print(f"현재가 : ${close:.2f}")
    print(f"전일대비 : {change:+.2f}%")
    print(f"목표가까지 : {target_gap:+.2f}%")
    print("-" * 40)

print("KOBA Watch 실행 완료")