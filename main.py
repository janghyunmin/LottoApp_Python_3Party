import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def fetch_lotto_numbers(draw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={draw_no}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["returnValue"] == "success":
            result = {
                "totSellamnt": data["totSellamnt"],
                "returnValue": data["returnValue"],
                "drwNoDate": data["drwNoDate"],
                "firstWinamnt": data["firstWinamnt"],
                "drwtNo6": data["drwtNo6"],
                "drwtNo4": data["drwtNo4"],
                "firstPrzwnerCo": data["firstPrzwnerCo"],
                "drwtNo5": data["drwtNo5"],
                "bnusNo": data["bnusNo"],
                "firstAccumamnt": data["firstAccumamnt"],
                "drwNo": data["drwNo"],
                "drwtNo2": data["drwtNo2"],
                "drwtNo3": data["drwtNo3"],
                "drwtNo1": data["drwtNo1"]
            }
            return result
    return None

def get_recent_lotto_numbers():
    recent_lotto_numbers = []
    url = "https://www.dhlottery.co.kr/common.do?method=main"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    latest_draw_no = int(soup.select_one("#lottoDrwNo").text.strip())

    today = datetime.today()
    one_year_ago = today - timedelta(days=365)

    for draw_no in range(latest_draw_no, 0, -1):
        result = fetch_lotto_numbers(draw_no)
        if result:
            draw_date = datetime.strptime(result["drwNoDate"], "%Y-%m-%d")
            if draw_date < one_year_ago:
                break
            recent_lotto_numbers.append(result)

    return recent_lotto_numbers

if __name__ == "__main__":
    recent_lotto_numbers = get_recent_lotto_numbers()
    for result in recent_lotto_numbers:
        print(json.dumps(result, ensure_ascii=False, indent=2))
