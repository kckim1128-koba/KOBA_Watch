import json
import os
from datetime import datetime
import requests

from config import (
    STOCKS,
    MARKET_ITEMS,
    RSI_OVERBOUGHT,
    RSI_OVERSOLD,
    SURGE_ALERT,
    DROP_ALERT,
    USE_NEWS,
    USE_AI,
    USE_KAKAO,
)
from market import get_latest_price_info
from indicator import get_rsi, get_rsi_status
from ai import make_ai_comment
from news import get_news_summary


ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN", "").strip()
REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN", "").strip()
REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "").strip()


def refresh_access_token():
    if not REFRESH_TOKEN or not REST_API_KEY:
        print("❌ Refresh Token 또는 REST API Key가 없습니다.")
        return None

    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": REFRESH_TOKEN,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    print("🔄 토큰 갱신 결과")
    print(tokens)

    return tokens.get("access_token")


def get_move_status(change):
    if change >= SURGE_ALERT:
        return f"🚀 {SURGE_ALERT}% 이상 급등"
    elif change <= DROP_ALERT:
        return f"⚠️ {abs(DROP_ALERT)}% 이상 급락"
    return ""


def build_stock_section():
    text = ""
    stock_summaries = []

    for symbol, info in STOCKS.items():
        price_info = get_latest_price_info(symbol)

        if price_info is None:
            text += f"⚪ {info['name']}\n데이터 부족\n\n"
            continue

        data = price_info["data"]
        close = price_info["close"]
        change = price_info["change"]
        target_gap = (info["target"] - close) / close * 100
        rsi = get_rsi(data)

        icon = "🟢" if change >= 0 else "🔴"
        move_status = get_move_status(change)
        rsi_status = get_rsi_status(rsi, RSI_OVERBOUGHT, RSI_OVERSOLD)

        text += f"{icon} {info['name']}\n"
        text += f"현재가 : ${close:,.2f}\n"
        text += f"전일대비 : {change:+.2f}%\n"
        text += f"목표가까지 : {target_gap:+.2f}%\n"
        text += f"RSI : {rsi:.0f} {rsi_status}\n"

        if move_status:
            text += f"{move_status}\n"

        text += "\n"

        stock_summaries.append({
            "symbol": symbol,
            "name": info["name"],
            "close": close,
            "change": change,
            "target_gap": target_gap,
            "rsi": rsi,
        })

    return text, stock_summaries


def build_market_section():
    text = ""
    market_summaries = []

    for symbol, name in MARKET_ITEMS.items():
        price_info = get_latest_price_info(symbol)

        if price_info is None:
            text += f"{name} : 데이터 부족\n"
            continue

        close = price_info["close"]
        change = price_info["change"]
        icon = "🟢" if change >= 0 else "🔴"

        text += f"{icon} {name} : {close:.2f} ({change:+.2f}%)\n"

        market_summaries.append({
            "symbol": symbol,
            "name": name,
            "close": close,
            "change": change,
        })

    sp = next((x for x in market_summaries if x["name"] == "S&P500"), None)
    nasdaq = next((x for x in market_summaries if x["name"] == "NASDAQ"), None)
    sox = next((x for x in market_summaries if x["name"] == "SOX"), None)
    vix = next((x for x in market_summaries if x["name"] == "VIX"), None)

    summary = ""

    if sp and nasdaq:
        if sp["change"] > 0 and nasdaq["change"] > 0:
            summary = "📈 미국 증시는 전반적으로 강세"
        elif sp["change"] < 0 and nasdaq["change"] < 0:
            summary = "📉 미국 증시는 전반적으로 약세"
        else:
            summary = "➖ 미국 증시는 혼조세"

    if sox:
        if sox["change"] > 1:
            summary += " · 반도체 강세"
        elif sox["change"] < -1:
            summary += " · 반도체 약세"

    if vix:
        if vix["change"] < 0:
            summary += " · 변동성 감소"
        elif vix["change"] > 0:
            summary += " · 변동성 확대"

    if summary:
        text += f"\n📝 {summary}\n"

    text += "\n"
    return text, market_summaries


def make_message():
    message = ""
    message += "📈 KOBA Watch\n"
    message += "Keep Observing, Build Assets.\n"
    message += "────────────────\n\n"

    stock_text, stock_summaries = build_stock_section()
    market_text, market_summaries = build_market_section()

    message += "🌎 간밤 미국시장\n\n"
    message += market_text

    message += "────────────────\n\n"

    message += "🎯 내 관심종목\n\n"
    message += stock_text

    if USE_NEWS:
        message += get_news_summary()

    if USE_AI:
        message += make_ai_comment(stock_summaries, market_summaries)

    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

    return message


def send_message(message):
    if not USE_KAKAO:
        print(message)
        return

    if not ACCESS_TOKEN:
        raise ValueError("KAKAO_ACCESS_TOKEN Secret이 없습니다.")

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

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

    def post_to_kakao(token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        return requests.post(url, headers=headers, data=data)

    response = post_to_kakao(ACCESS_TOKEN)

    if response.status_code == 401:
        print("⚠️ Access Token 만료 감지, 갱신 시도")
        new_access_token = refresh_access_token()

        if new_access_token:
            response = post_to_kakao(new_access_token)

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