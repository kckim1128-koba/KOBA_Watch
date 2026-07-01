from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

key = os.getenv("KAKAO_REST_API_KEY")

if key:
    print("✅ REST API Key 읽기 성공")
else:
    print("❌ REST API Key 읽기 실패")