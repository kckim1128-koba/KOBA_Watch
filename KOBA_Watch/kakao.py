import os
from pathlib import Path

ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    token_path = Path(__file__).parent / "kakao_token.txt"
    with open(token_path, "r", encoding="utf-8") as f:
        ACCESS_TOKEN = f.read().strip()