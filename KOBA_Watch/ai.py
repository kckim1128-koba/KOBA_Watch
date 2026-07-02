def make_ai_comment(stock_summaries=None, market_summary=None):
    """
    KOBA AI v1
    - OpenAI API 없이 조건 기반으로 시장 코멘트 생성
    - 나중에 GPT API 연결 시 이 파일만 업그레이드
    """

    if stock_summaries is None:
        stock_summaries = []

    comments = []

    # 급등 종목 확인
    surge_stocks = [
        item for item in stock_summaries
        if item.get("change", 0) >= 5
    ]

    # 급락 종목 확인
    drop_stocks = [
        item for item in stock_summaries
        if item.get("change", 0) <= -5
    ]

    # 과매수 종목 확인
    overbought_stocks = [
        item for item in stock_summaries
        if item.get("rsi") is not None and item.get("rsi") >= 70
    ]

    # 과매도 종목 확인
    oversold_stocks = [
        item for item in stock_summaries
        if item.get("rsi") is not None and item.get("rsi") <= 30
    ]

    if surge_stocks:
        names = ", ".join([item["name"] for item in surge_stocks])
        comments.append(f"{names}가 5% 이상 상승했습니다. 단기 급등 구간이므로 추격매수보다는 변동성 확인이 필요합니다.")

    if drop_stocks:
        names = ", ".join([item["name"] for item in drop_stocks])
        comments.append(f"{names}가 5% 이상 하락했습니다. 단기 충격 구간이지만 RSI와 시장 분위기를 함께 확인할 필요가 있습니다.")

    if overbought_stocks:
        names = ", ".join([item["name"] for item in overbought_stocks])
        comments.append(f"{names}의 RSI가 과매수 구간에 진입했습니다. 단기 조정 가능성에 유의하는 것이 좋습니다.")

    if oversold_stocks:
        names = ", ".join([item["name"] for item in oversold_stocks])
        comments.append(f"{names}의 RSI가 과매도 구간입니다. 장기 관점에서는 분할 접근을 검토할 수 있습니다.")

    if not comments:
        comments.append("관심 종목들은 과열이나 급락 신호 없이 비교적 안정적인 흐름입니다. 오늘은 시장 지표와 반도체 업종 방향성을 함께 확인하는 것이 좋습니다.")

    return "🤖 KOBA AI 의견\n" + "\n".join(comments[:2]) + "\n\n"