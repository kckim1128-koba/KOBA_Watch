# KOBA Watch Project Status

## 프로젝트 목적

KOBA Watch는 미국 시장 정보를 자동 분석하여
예약 시간 또는 수동 실행 시 카카오톡으로 전달하는 개인 투자 브리핑 시스템이다.

---

## 현재 버전

KOBA v1.2

---

## 현재 구조

- config.py : 설정
- market.py : Yahoo Finance 조회
- indicator.py : RSI 계산
- news.py : 뉴스
- ai.py : AI 브리핑
- send_kakao.py : 카카오톡 발송
- main.py : 메인 실행
- tray.py : Tray + Scheduler + 수동 실행
- start_koba.bat : 프로그램 시작

---

## 완료

- GitHub 연동
- 카카오 API 연동
- Yahoo Finance 연동
- RSI 계산
- AI 의견
- Tray 실행
- 예약 실행
- 수동 실행
- VS 없이 실행
- BAT 실행
- 로그 저장

---

## 현재 남은 작업

- 검은 CMD창 1초 제거
- 시작프로그램 자동 등록
- config.py에서 예약시간 관리
- 뉴스 기능 고도화
- GPT 브리핑 고도화

---

## 개발 원칙

1. tray.py만 실행한다.
2. Scheduler는 tray.py에서 관리한다.
3. 완료 후 Git Commit & Push.
4. 정상 동작 확인 후 다음 기능 개발.