#!/usr/bin/env python3
import urllib.request, urllib.parse, json, sys

TOKEN = "8831223977:AAFo43U9KuPszrzFN7er1JGV6ADwTmYN2NI"
YURI_CHAT_ID = 8269258729

def send_ping(message_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": YURI_CHAT_ID, "text": message_text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        return res.get("ok", False)
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "🚀 [ИИ-СТОРОЖ GITHUB] Автоматический сигнал Сторожа!"
    success = send_ping(text)
    print("Delivery Status:", success)
