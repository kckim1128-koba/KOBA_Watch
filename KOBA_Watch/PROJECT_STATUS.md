# KOBA Watch Project Status

## 프로젝트 목적
KOBA Watch는 매일 아침 미국 시장과 관심 종목을 요약하여 카카오톡으로 보내주는 개인 투자 브리핑 시스템이다.

## 현재 목표
자동 실행보다 먼저 프로젝트 기틀을 안정화한다.
수동 실행 시 카카오톡이 정상 발송되는 v1.0 구조를 만든다.

## 현재 구조
- config.py : 종목, 목표가, RSI 기준, 기능 ON/OFF 설정
- market.py : Yahoo Finance 시세 조회
- indicator.py : RSI 계산
- news.py : 뉴스 기능 자리
- ai.py : 조건 기반 AI 의견
- send_kakao.py : 메시지 생성 및 카카오톡 발송
- main.py : 전체 실행 시작

## 완료
- Python / Git / VS Code 설치
- GitHub Repository 생성
- 카카오 API 연동
- Access Token 재발급 성공
- GitHub Secret 등록
- 수동 실행 시 카카오톡 발송 성공
- data / logs / tools 폴더 생성
- config.py 정리
- market.py 정리
- indicator.py 정리
- ai.py v1 작성
- news.py 기본 작성
- send_kakao.py 정리
- main.py 정리

## 미완료
- README.md 정리
- GitHub 저장
- v1.0 기준점 생성
- 뉴스 기능
- GPT AI 브리핑
- 자동 실행

## 개발 원칙
1. 한 번에 한 파일만 수정한다.
2. 정상 동작 확인 후 commit 한다.
3. 자동 실행은 마지막에 한다.
4. 카톡이 안 오면 먼저 GitHub Actions 로그와 KAKAO_ACCESS_TOKEN을 확인한다.