import json
import os
from datetime import datetime
import requests

from config import STOCKS, MARKET_ITEMS
from market import get_latest_price_info
from indicator import get_rsi
from ai import make_ai_comment
from news import get_news_summary


ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN", "").strip()


def get_rsi_status(rsi):
    if rsi >= 70:
        return "🔥 과매수 주의"
    elif rsi <= 30:
        return "💥 과매도 구간"
    return "보통"


def get_move_status(change):
    if change >= 5:
        return "🚀 5% 이상 급등"
    elif change <= -5:
        return "⚠️ 5% 이상 급락"
    return ""


def get_stock_summary(symbol, info):
    price_info = get_latest_price_info(symbol)

    if price_info is None:
        return f"⚪ {info['name']}\n데이터 부족\n\n"

    data = price_info["data"]
    close = price_info["close"]
    change = price_info["change"]
    target_gap = (info["target"] - close) / close * 100
    rsi = get_rsi(data)

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
    text = "📊 시장 체크\n"

    for symbol, name in MARKET_ITEMS.items():
        price_info = get_latest_price_info(symbol)

        if price_info is None:
            text += f"{name} : 데이터 부족\n"
            continue

        close = price_info["close"]
        change = price_info["change"]
        text += f"{name} : {close:.2f} ({change:+.2f}%)\n"

    text += "\n"
    return text


def make_message():
    message = ""
    message += "📈 KOBA Watch\n"
    message += "Keep Observing, Build Assets.\n"
    message += "────────────────\n\n"
    message += "🚨 해외주식 알림\n\n"

    for symbol, info in STOCKS.items():
        message += get_stock_summary(symbol, info)

    message += get_market_summary()
    message += get_news_summary()
    message += make_ai_comment()
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

    return message


def send_message(message):
    if not ACCESS_TOKEN:
        raise ValueError("KAKAO_ACCESS_TOKEN Secret이 없습니다.")

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
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
        "template_object": json.dumps(template_object, ensure_ascii=False)
    }

    response = requests.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        print("✅ KOBA Watch 알림 전송 성공")
    else:
        print("❌ 전송 실패")


def run():
    message = make_message()
    send_message(message)


if __name__ == "__main__":
    run()