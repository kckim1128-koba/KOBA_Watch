from pathlib import Path
from datetime import datetime
import requests
import yfinance as yf
from ta.momentum import RSIIndicator

TOKEN_PATH = Path(__file__).parent / "kakao_token.txt"

with open(TOKEN_PATH, "r", encoding="utf-8") as f:
    ACCESS_TOKEN = f.read().strip()

stocks = {
    "MUU": {
        "name": "MUU (Micron 2X)",
        "target": 1500,
    },
    "SNXX": {
        "name": "SNXX",
        "target": 100,
    },
    "SOXL": {
        "name": "SOXL",
        "target": 400,
    },
}

def get_rsi_status(rsi):
    if rsi >= 70:
        return "🔥 과매수 주의"
    elif rsi <= 30:
        return "💥 과매도 구간"
    else:
        return "보통"

def get_move_status(change):
    if change >= 5:
        return "🚀 5% 이상 급등"
    elif change <= -5:
        return "⚠️ 5% 이상 급락"
    else:
        return ""

def get_stock_summary(symbol, info):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="3mo")

    if data.empty or len(data) < 20:
        return f"⚪ {info['name']}\n데이터 부족\n\n"

    close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]
    change = (close - prev_close) / prev_close * 100
    target_gap = (info["target"] - close) / close * 100
    rsi = RSIIndicator(close=data["Close"], window=14).rsi().iloc[-1]

    icon = "🟢" if change >= 0 else "🔴"
    move_status = get_move_status(change)

    text = ""
    text += f"{icon} {info['name']}\n"
    text += f"현재가 : ${close:,.2f}\n"
    text += f"전일대비 : {change:+.2f}%\n"
    text += f"목표가까지 : {target_gap:+.2f}%\n"
    text += f"RSI : {rsi:.0f} {get_rsi_status(rsi)}\n"

    if move_status:
        text += f"{move_status}\n"

    text += "\n"

    return text

def get_market_summary():
    market_items = {
        "^VIX": "VIX",
        "^SOX": "SOX",
    }

    text = "📊 시장 체크\n"

    for symbol, name in market_items.items():
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")

        if data.empty or len(data) < 2:
            text += f"{name} : 데이터 부족\n"
            continue

        close = data["Close"].iloc[-1]
        prev_close = data["Close"].iloc[-2]
        change = (close - prev_close) / prev_close * 100

        text += f"{name} : {close:.2f} ({change:+.2f}%)\n"

    text += "\n"
    return text

def make_ai_comment():
    return (
        "🤖 AI 한 줄 의견\n"
        "반도체 흐름은 강하지만 단기 급등 종목은 RSI와 목표가까지의 거리를 함께 확인하는 것이 좋습니다.\n\n"
    )

message = ""
message += "📈 KOBA Watch\n"
message += "Keep Observing, Build Assets.\n"
message += "────────────────\n\n"
message += "🚨 해외주식 알림\n\n"

for symbol, info in stocks.items():
    message += get_stock_summary(symbol, info)

message += get_market_summary()
message += make_ai_comment()
message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

template_object = {
    "object_type": "text",
    "text": message,
    "link": {
        "web_url": "https://finance.yahoo.com",
        "mobile_web_url": "https://finance.yahoo.com",
    },
    "button_title": "Yahoo Finance",
}

data = {
    "template_object": str(template_object).replace("'", '"')
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.text)

if response.status_code == 200:
    print("✅ KOBA Watch 알림 전송 성공")
else:
    print("❌ 전송 실패")