#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Сменный ИИ-Агент Автоматизации
Назначение: Парсинг логов смены, генерация журналов и прицепов памяти через Gemini Flash API.
"""

import os
import sys
import json
import glob
import re
import shutil
import urllib.request
import urllib.error
from datetime import datetime

# Configuration of targets
BASE_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН"
SHIFT_JOURNAL_RU_PATH = os.path.join(BASE_DIR, "СМЕННЫЙ_ЖУРНАЛ.md")
SHIFT_LOG_EN_PATH = os.path.join(BASE_DIR, "SHIFT_LOG.md")
SHIFT_TRAILER_RU_PATH = os.path.join(BASE_DIR, "СМЕННЫЙ_ПРИЦЕП.md")
DAILY_TRAILER_EN_PATH = os.path.join(BASE_DIR, "DAILY_TRAILER.md")
MEMORY_FULL_RU_PATH = os.path.join(BASE_DIR, "ПРИЦЕП_ПАМЯТИ_FULL.md")
MEMORY_FULL_EN_PATH = os.path.join(BASE_DIR, "MEMORY_TRAILER.md")

def get_gemini_api_key():
    # 1. Check environment variable
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key

    # 2. Check keys.json fallback
    config_path = os.path.expanduser("~/.gemini/config/keys.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Check direct keys
                for k in ["GEMINI_API_KEY", "gemini_api_key", "api_key"]:
                    if k in data and data[k]:
                        return data[k]
                # Check nested keys
                if "gemini" in data and isinstance(data["gemini"], dict):
                    if "api_key" in data["gemini"] and data["gemini"]["api_key"]:
                        return data["gemini"]["api_key"]
                if "google" in data and isinstance(data["google"], dict):
                    if "api_key" in data["google"] and data["google"]["api_key"]:
                        return data["google"]["api_key"]
        except Exception:
            pass

    # 3. Check Monolith backend .env file fallback
    env_path = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/06_ЦЕХ_МОНОЛИТ/backend/.env"
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        val = line.strip().split("=", 1)[1].strip()
                        if val:
                            return val
        except Exception:
            pass

    return None

def find_latest_transcript():
    pattern = os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl"
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError("Не найден ни один файл transcript.jsonl в каталогах /Users/tur/.gemini/antigravity/brain/*/")
    
    # Return the one with the latest mtime
    return max(files, key=os.path.getmtime)

def parse_transcript(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл лога диалога не найден: {file_path}")

    messages = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    messages.append(msg)
                except Exception:
                    pass
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения файла логов: {e}")

    # Find the last cutoff occurrence of "/start_shift" or "открываем рабочий день"
    cutoff_index = -1
    for idx, msg in enumerate(messages):
        content = msg.get("content", "") or ""
        if "/start_shift" in content or "открываем рабочий день" in content.lower():
            # Skip matches that are instructions detailing the task
            if "requirements for" in content.lower() or "shift_agent.py" in content.lower():
                continue
            cutoff_index = idx

    # Filter messages after the cutoff that are USER_INPUT or PLANNER_RESPONSE
    filtered = []
    for msg in messages[cutoff_index + 1:]:
        msg_type = msg.get("type")
        if msg_type in ["USER_INPUT", "PLANNER_RESPONSE"]:
            filtered.append(msg)

    # Fallback: if no messages found after cutoff, use all USER_INPUT and PLANNER_RESPONSE
    if not filtered:
        filtered = [msg for msg in messages if msg.get("type") in ["USER_INPUT", "PLANNER_RESPONSE"]]

    return filtered

def format_messages_for_prompt(messages):
    formatted = []
    for msg in messages:
        role = "USER" if msg.get("type") == "USER_INPUT" else "ASSISTANT"
        content = msg.get("content", "") or ""
        formatted.append(f"[{role}]: {content.strip()}")
    return "\n\n".join(formatted)

def call_gemini_flash(api_key, conversation_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    
    prompt = f"""You are the Lead AI-Architect. Analyze the following conversation transcript of the current shift.
The transcript contains messages between the USER and the ASSISTANT.

Conversation transcript:
{conversation_text}

Generate a JSON object containing the following keys:
1. "shift_journal_ru": Russian text for СМЕННЫЙ_ЖУРНАЛ.md (summary of achievements and timeline of events of the current shift).
2. "shift_log_en": English translation of shift_journal_ru for SHIFT_LOG.md.
3. "shift_trailer_ru": Russian text for СМЕННЫЙ_ПРИЦЕП.md (current coordinates of the assembly, active cabin status, what is verified).
4. "daily_trailer_en": English translation of shift_trailer_ru for DAILY_TRAILER.md.
5. "memory_trailer_ru": Russian log block to append to ПРИЦЕП_ПАМЯТИ_FULL.md. Do NOT include any block header or date. Just write the list of actions and next steps.
6. "memory_trailer_en": English log block to append to MEMORY_TRAILER.md. Do NOT include any block header or date. Just write the list of actions and next steps.

Make sure the Russian text matches the tone and rules of Constructor-Architect Pro:
- Zero jargon in dialogue (use analogies of houses, conveyors, paper tickets, physical locks, dashboards instead of network protocols, pipelines, APIs).
- High visual aesthetics and premium style for markdown files.
- Always link key documents in Obsidian format using double square brackets (e.g. [[ПРИЦЕП_ПАМЯТИ_FULL]], [[СМЕННЫЙ_ЖУРНАЛ]], [[ПОВЕСТКА_ПЛАНЕРКИ]], [[ANTIGRAVITY]]) in Russian texts to create a connected knowledge graph.
- ALWAYS write highly detailed reports on the completed assembly work in projects (especially Monolith), specifying the exact errors fixed, typos corrected, database schema updates made, and test results, so that the General Designer (Yuri) can easily conduct audits without having to inspect raw code.

Respond ONLY with a valid JSON object matching this schema:
{{
  "shift_journal_ru": "string",
  "shift_log_en": "string",
  "shift_trailer_ru": "string",
  "daily_trailer_en": "string",
  "memory_trailer_ru": "string",
  "memory_trailer_en": "string"
}}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "shift_journal_ru": {"type": "STRING"},
                    "shift_log_en": {"type": "STRING"},
                    "shift_trailer_ru": {"type": "STRING"},
                    "daily_trailer_en": {"type": "STRING"},
                    "memory_trailer_ru": {"type": "STRING"},
                    "memory_trailer_en": {"type": "STRING"}
                },
                "required": [
                    "shift_journal_ru",
                    "shift_log_en",
                    "shift_trailer_ru",
                    "daily_trailer_en",
                    "memory_trailer_ru",
                    "memory_trailer_en"
                ]
            }
        }
    }
    
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            res_json = json.loads(res_body)
            text_out = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            # Remove potential markdown block wrappers
            if text_out.startswith("```"):
                lines = text_out.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                text_out = "\n".join(lines).strip()
                
            return json.loads(text_out)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API HTTP Error {e.code}: {e.reason}\nResponse: {err_body}")
    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {str(e)}")

def find_next_block_index(file_path):
    if not os.path.exists(file_path):
        return 1
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        pattern = re.compile(r'(?:Block|БЛОК)\s*#?\s*(\d+)', re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            return max(int(m) for m in matches) + 1
    except Exception:
        pass
    return 1

def backup_and_write(path, content, append=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        bak_path = path + ".bak"
        try:
            shutil.copy2(path, bak_path)
        except Exception as e:
            raise RuntimeError(f"Не удалось создать резервную копию для {os.path.basename(path)}: {e}")
            
    mode = "a" if append else "w"
    try:
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise RuntimeError(f"Не удалось записать в {os.path.basename(path)}: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Сменный ИИ-Агент Constructor-Architect Pro")
    parser.add_argument("--dry-run", action="store_true", help="Режим имитации: вывести JSON и не менять файлы")
    args = parser.parse_args()

    try:
        # Resolve API Key
        api_key = get_gemini_api_key()
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY не найдена ни в переменных окружения, ни в ~/.gemini/config/keys.json")

        # Find latest transcript
        latest_transcript = find_latest_transcript()
        print(f"🔍 Найден последний лог диалога: {latest_transcript}")

        # Parse messages
        messages = parse_transcript(latest_transcript)
        print(f"📊 Выделено реплик для анализа: {len(messages)}")

        if not messages:
            raise RuntimeError("Нет реплик для отправки в Gemini")

        # Format messages for prompt
        conversation_text = format_messages_for_prompt(messages)

        # Call Gemini API
        print("🚀 Отправка запроса в Gemini Flash...")
        response_data = call_gemini_flash(api_key, conversation_text)
        print("✅ Ответ от Gemini Flash успешно получен и разобран.")

        if args.dry_run:
            print("\n=== ИМИТАЦИЯ ЗАПУСКА (--dry-run) ===")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            print("====================================")
            sys.exit(0)

        # Write updates
        print("💾 Запись обновлений на диск с созданием резервных копий...")

        # Overwrite journals and trailers
        backup_and_write(SHIFT_JOURNAL_RU_PATH, response_data["shift_journal_ru"])
        backup_and_write(SHIFT_LOG_EN_PATH, response_data["shift_log_en"])
        backup_and_write(SHIFT_TRAILER_RU_PATH, response_data["shift_trailer_ru"])
        backup_and_write(DAILY_TRAILER_EN_PATH, response_data["daily_trailer_en"])

        # Determine block index for append files
        next_block = find_next_block_index(MEMORY_FULL_RU_PATH)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Append block headers & content
        block_header = f"\n\n## Block {next_block} - {current_time}\n"
        
        append_ru = block_header + response_data["memory_trailer_ru"].strip() + "\n"
        append_en = block_header + response_data["memory_trailer_en"].strip() + "\n"

        backup_and_write(MEMORY_FULL_RU_PATH, append_ru, append=True)
        backup_and_write(MEMORY_FULL_EN_PATH, append_en, append=True)

        # Reset active cabin to NEUTRAL upon shift closure for clean state in next chat session
        active_cabin_path = os.path.join(BASE_DIR, "ACTIVE_CABIN.txt")
        try:
            with open(active_cabin_path, "w", encoding="utf-8") as cabin_f:
                cabin_f.write("NEUTRAL\n")
            print("🔒 ACTIVE_CABIN.txt reset to NEUTRAL for next chat session clean start.")
        except Exception as e:
            print(f"Warning: Failed to reset active cabin: {e}")

        print(f"🎉 Смена успешно автоматизирована! Блок {next_block} записан.")

    except Exception as e:
        print(f"🔴 КРИТИЧЕСКАЯ ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
