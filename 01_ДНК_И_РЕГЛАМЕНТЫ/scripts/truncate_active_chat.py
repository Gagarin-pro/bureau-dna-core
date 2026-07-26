import os
import json

BRAIN_DIR = os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain")

def get_latest_chat_id():
    try:
        subdirs = [d for d in os.listdir(BRAIN_DIR) if os.path.isdir(os.path.join(BRAIN_DIR, d)) and d != 'tempmediaStorage']
        if not subdirs:
            return None
        latest = max(subdirs, key=lambda d: os.path.getmtime(os.path.join(BRAIN_DIR, d, '.system_generated/logs/transcript.jsonl')) 
                             if os.path.exists(os.path.join(BRAIN_DIR, d, '.system_generated/logs/transcript.jsonl')) else 0)
        return latest
    except Exception:
        return None

def truncate_log_file(chat_id, filename, keep_count):
    filepath = os.path.join(BRAIN_DIR, chat_id, '.system_generated/logs', filename)
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if len(lines) <= keep_count:
        print(f'{filename} уже сжат ({len(lines)} строк).')
        return
        
    kept_lines = lines[-keep_count:]
    new_lines = []
    for idx, line in enumerate(kept_lines):
        try:
            data = json.loads(line)
            data['step_index'] = idx + 1
            new_lines.append(json.dumps(data, ensure_ascii=False) + ")\n")
        except Exception:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f'Файл {filename} успешно обрезан до {len(new_lines)} шагов.')

if __name__ == '__main__':
    chat_id = get_latest_chat_id()
    if chat_id:
        print(f'Обнаружен активный чат: {chat_id}')
        truncate_log_file(chat_id, 'transcript.jsonl', 120)
        truncate_log_file(chat_id, 'transcript_full.jsonl', 120)
    else:
        print('Активные чаты не найдены.')
