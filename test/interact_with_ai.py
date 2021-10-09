import requests
import json


API_KEY = "AI7R3SC7DvSBsP79m7oCfdzUdcKV98GA"
CLIENT_ID = "qn1042402"
AI_ID = "AI"
LNG = "ru"
FULLNAME = "test"


def get_ai_response(message):
    url = f"https://qaim.me/userapi/ai/{API_KEY}/"
    payload = dict(
        data=json.dumps(dict(
            q=message,
            ai=AI_ID,
            client_id=CLIENT_ID,
            lng=LNG,
            fullname=FULLNAME,
        ),
            ensure_ascii=False
        )
    )
    print(payload)

    r = requests.post(url, data=payload)

    return r, r.text


if __name__ == "__main__":
    msg = "А так? )))"
    print(get_ai_response(msg))
