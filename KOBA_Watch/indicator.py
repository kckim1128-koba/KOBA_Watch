from ta.momentum import RSIIndicator


def get_rsi(data):
    if data is None or data.empty or len(data) < 20:
        return None

    rsi = RSIIndicator(close=data["Close"], window=14).rsi()
    return float(rsi.iloc[-1])


def get_rsi_status(rsi, overbought=70, oversold=30):
    if rsi is None:
        return "데이터 부족"

    if rsi >= overbought:
        return "🔥 과매수 주의"
    elif rsi <= oversold:
        return "💥 과매도 구간"
    else:
        return "보통"