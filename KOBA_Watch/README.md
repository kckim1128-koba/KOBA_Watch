# KOBA Watch

**Keep Observing, Build Assets.**

해외주식 자동 모니터링 및 카카오톡 알림 시스템

---

## 프로젝트 목적

GitHub Actions를 이용하여 PC를 켜두지 않아도
매일 자동으로 미국 주식 및 시장 정보를 수집하여
카카오톡으로 전송하는 시스템

---

## 현재 기능

- 해외주식 시세 조회 (Yahoo Finance)
- 전일 대비 등락률 계산
- 목표가까지 남은 비율 계산
- RSI 계산
- 시장지수 확인
- AI 코멘트 출력
- 카카오톡 나에게 자동 전송
- GitHub Actions 자동 실행

---

## 프로젝트 구조

```
PROJECT KOBA
│
├── .github
│   └── workflows
│       └── koba_watch.yml
│
└── KOBA_Watch
    ├── main.py
    ├── config.py
    ├── market.py
    ├── indicator.py
    ├── send_kakao.py
    ├── news.py
    ├── ai.py
    └── requirements.txt
```

---

## 실행 흐름

```
GitHub Actions
        │
        ▼
main.py
        │
        ▼
market.py
indicator.py
        │
        ▼
메시지 생성
        │
        ▼
send_kakao.py
        │
        ▼
Kakao API
        │
        ▼
카카오톡 "나에게"
```

---

## 주요 파일

| 파일 | 설명 |
|------|------|
| main.py | 프로그램 시작 |
| config.py | 종목 및 목표가 설정 |
| market.py | Yahoo Finance 데이터 조회 |
| indicator.py | RSI 계산 |
| send_kakao.py | 카카오톡 메시지 생성 및 전송 |
| news.py | 뉴스 수집 (예정) |
| ai.py | AI 분석 (예정) |
| requirements.txt | Python 라이브러리 |
| koba_watch.yml | GitHub Actions 자동 실행 |

---

## 자동 실행

GitHub Actions

- UTC 22:00
- 한국시간 오전 07:00

---

## GitHub Secret

필수 Secret

```
KAKAO_ACCESS_TOKEN
```

Bearer 없이

```
xxxxxxxxxxxxxxxxxxxxxxxx
```

토큰 문자열만 저장

---

## 현재 모니터링 종목

- MU
- SNXX
- SOXL

---

## 개발 예정 (Roadmap)

### v1.1
- 뉴스 요약

### v1.2
- AI 시장 분석

### v1.3
- 환율
- VIX
- SOX Index

### v1.4
- 목표가 도달 알림

### v1.5
- RSI 과매수/과매도 알림

### v2.0
- AI 투자 비서
- 시장 브리핑 자동 생성
- 종목별 투자 의견