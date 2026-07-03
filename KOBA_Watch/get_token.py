from dotenv import load_dotenv
from pathlib import Path
import os
import requests

load_dotenv(Path(__file__).parent / ".env")

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
REDIRECT_URI = "http://localhost:8080"

AUTH_CODE = "BCQT_rgQpWWuIo-czUeFIMYNFHEE5WtuELt1rHamdqASoYFM6r4V-gAAAAQKFxJVAAABnyU0qvtDz1szkZmFRA"

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

    if "refresh_token" in tokens:
        with open(Path(__file__).parent / "kakao_refresh_token.txt", "w", encoding="utf-8") as f:
            f.write(tokens["refresh_token"])

    print("✅ Access Token 저장 성공")
    print("✅ Refresh Token 저장 성공")
else:
    print("❌ Access Token 발급 실패")