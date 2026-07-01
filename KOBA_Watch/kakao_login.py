from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from pathlib import Path
import webbrowser

load_dotenv(Path(__file__).parent / ".env")

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

REDIRECT_URI = "http://localhost:8080"

params = {
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "talk_message"
}

url = "https://kauth.kakao.com/oauth/authorize?" + urlencode(params)

print("브라우저를 엽니다...")
print(url)

webbrowser.open(url)