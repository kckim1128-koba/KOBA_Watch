from dotenv import load_dotenv
from pathlib import Path
import os
import requests

load_dotenv(Path(__file__).parent / ".env")

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
REDIRECT_URI = "http://localhost:8080"

AUTH_CODE = "ZL8s7mrg5MI5gr89tr5_VpBwmCd_94tY1hMMRlz-WfJmtXx25XbZygAAAAQKDRSjAAABnxtpNhWoblpFv_zasg"

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE,
}

response = requests.post(url, data=data)
tokens = response.json()

print(tokens)

if "access_token" in tokens:
    with open(Path(__file__).parent / "kakao_token.txt", "w", encoding="utf-8") as f:
        f.write(tokens["access_token"])

    print("✅ Access Token 저장 성공")
else:
    print("❌ Access Token 발급 실패")