# ==========================================
# KOBA Watch 설정 파일
# ==========================================

# 감시 종목
STOCKS = {
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

# 시장 지표
MARKET_ITEMS = {
    "^VIX": "VIX",
    "^SOX": "SOX",
}

# RSI 기준
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# 급등 / 급락 기준
SURGE_ALERT = 5
DROP_ALERT = -5

# 기능 사용 여부
USE_NEWS = True
USE_AI = True
USE_KAKAO = True