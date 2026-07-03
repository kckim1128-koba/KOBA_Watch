import threading
import subprocess
import time
from pathlib import Path
from datetime import datetime

import schedule
import pystray
from PIL import Image, ImageDraw


BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "koba_tray.log"

AUTO_TIMES = ["16:05"]  # 테스트 시간, 나중에 ["08:00"]


def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def run_koba():
    log("KOBA Watch 실행 시작")

    env = dict()
    import os
    env.update(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        ["py", "-X", "utf8", "main.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    log(f"returncode={result.returncode}")
    log(result.stdout)
    log(result.stderr)


def scheduler_loop():
    log(f"Scheduler 시작 / 예약시간={AUTO_TIMES}")

    schedule.clear()

    for t in AUTO_TIMES:
        schedule.every().monday.at(t).do(run_koba)
        schedule.every().tuesday.at(t).do(run_koba)
        schedule.every().wednesday.at(t).do(run_koba)
        schedule.every().thursday.at(t).do(run_koba)
        schedule.every().friday.at(t).do(run_koba)

    while True:
        schedule.run_pending()
        time.sleep(1)


def create_icon_image():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill="green")
    draw.text((22, 22), "K", fill="white")
    return image


def on_run_now(icon, item):
    run_koba()


def on_exit(icon, item):
    log("KOBA Tray 종료")
    icon.stop()


def main():
    auto_text = ", ".join(AUTO_TIMES)

    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()

    icon = pystray.Icon(
        "KOBA Watch",
        create_icon_image(),
        f"KOBA Watch\n자동 브리핑 : 평일 {auto_text}",
        menu=pystray.Menu(
            pystray.MenuItem("● 실행 중", lambda icon, item: None, enabled=False),
            pystray.MenuItem(f"🕗 자동 브리핑 : 평일 {auto_text}", lambda icon, item: None, enabled=False),
            pystray.MenuItem("▶ 지금 실행", on_run_now),
            pystray.MenuItem("✖ 종료", on_exit),
        ),
    )

    icon.run()


if __name__ == "__main__":
    main()