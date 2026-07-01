# KOBA Watch

해외주식 자동 모니터링 및 카카오톡 알림 시스템

## 현재 기능
- MUU / SNXX / SOXL 시세 확인
- 전일 대비 등락률 확인
- 목표가까지 남은 비율 계산
- RSI 계산
- 카카오톡 나에게 보내기
- GitHub Actions 자동 실행

## 실행 흐름

GitHub Actions
→ KOBA_Watch/main.py
→ send_kakao.py
→ market.py / indicator.py
→ Kakao API
→ 카카오톡 알림

## 주요 파일

- main.py : 전체 실행 시작점
- config.py : 종목 및 목표가 설정
- market.py : Yahoo Finance 시세 조회
- indicator.py : RSI 계산
- send_kakao.py : 메시지 생성 및 카카오톡 발송
- requirements.txt : 필요한 Python 라이브러리 목록
- .github/workflows/koba_watch.yml : 자동 실행 설정

## 자동 실행 시간

현재 GitHub Actions 기준:

- UTC 22:00
- 한국시간 오전 07:00

## 다음 추가 예정
- 뉴스 요약
- AI 시장 코멘트
- 환율
- VIX / SOX
- 목표가 도달 알림
- RSI 과매수/과매도 알림