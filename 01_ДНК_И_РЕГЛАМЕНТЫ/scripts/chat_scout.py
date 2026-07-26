#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Чат-Стенографист» (Сенсор чата команды)
Назначение: Фоновый опрос Telegram API, логирование переписки разработчиков и передача отчетов в ИИ-Канал.
"""

import urllib.request
import urllib.parse
import json
import time
import os
import sys

TOKEN = "8723679369:AAECICguB6CtYC4xusweUd7wERgZpGvA0es"
LOG_FILE = "/home/tur/chat_scout.log"

def fetch_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
        
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка связи с Telegram API: {e}", file=sys.stderr)
        return None

def process_message(msg):
    chat = msg.get("chat", {})
    chat_type = chat.get("type")
    
    # Слушаем только групповые чаты и супергруппы
    if chat_type not in ["group", "supergroup"]:
        return
        
    chat_title = chat.get("title", "Рабочий чат")
    user = msg.get("from", {})
    username = user.get("username") or user.get("first_name") or "Неизвестный"
    text = msg.get("text")
    if not text:
        if "voice" in msg:
            duration = msg["voice"].get("duration", 0)
            text = f"🎙️ [Голосовое сообщение, {duration} сек]"
        elif "audio" in msg:
            title = msg["audio"].get("title", "Аудиозапись")
            text = f"🎵 [Аудио: {title}]"
        elif "photo" in msg:
            text = "📷 [Фотография]"
        elif "document" in msg:
            file_name = msg["document"].get("file_name", "Файл")
            text = f"📄 [Файл: {file_name}]"
        elif "sticker" in msg:
            emoji = msg["sticker"].get("emoji", "")
            text = f"👾 [Стикер {emoji}]"
        elif "video" in msg:
            text = "🎥 [Видеозапись]"
        else:
            text = "📦 [Неподдерживаемый тип сообщения]"
            
    date_ts = msg.get("date", time.time())
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date_ts))
    
    # Форматируем запись в лог-файл
    log_line = f"[{msg_time}] [{chat_title}] {username}: {text}\n"
    
    # Дозаписываем в файл
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"📝 Лог записан: {log_line.strip()}")
    except Exception as e:
        print(f"🔴 Ошибка записи лога: {e}", file=sys.stderr)

def main():
    print("🛸 Запуск Агента-Стенографиста чата...")
    print(f"📂 Файл логов: {LOG_FILE}")
    
    # Создаем файл если не существует
    if not os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"# 🧱 LOG INITIALIZED AT {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except Exception as e:
            print(f"🔴 Не удалось инициализировать файл лога: {e}", file=sys.stderr)
            sys.exit(1)
            
    offset = None
    
    while True:
        try:
            res_data = fetch_updates(offset)
            if res_data and res_data.get("ok"):
                updates = res_data.get("result", [])
                for u in updates:
                    update_id = u.get("update_id")
                    offset = update_id + 1
                    
                    message = u.get("message")
                    if message:
                        process_message(message)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Остановка Агента-Стенографиста.")
            break
        except Exception as e:
            print(f"⚠️ Ошибка в главном цикле: {e}", file=sys.stderr)
            time.sleep(5)

if __name__ == "__main__":
    main()
