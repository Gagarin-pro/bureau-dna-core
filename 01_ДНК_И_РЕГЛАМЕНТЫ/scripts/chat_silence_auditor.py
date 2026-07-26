import os, json, sys

def audit_chat_silence(brain_folder):
    log_file = os.path.join(brain_folder, ".system_generated/logs/transcript.jsonl")
    if not os.path.exists(log_file):
        return {"error": f"Log file not found: {log_file}"}
    
    left_chat_chars = 0
    right_dialogue_chars = 0
    other_tools_chars = 0
    total_model_responses = 0
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step_type = data.get("type", "")
                
                if step_type == "PLANNER_RESPONSE":
                    total_model_responses += 1
                    # Text emitted to left UI chat
                    left_text = str(data.get("content", ""))
                    left_chat_chars += len(left_text)
                    
                    # Inspect tool calls for РАБОЧИЙ_ДИАЛОГ.md
                    t_calls = data.get("tool_calls", [])
                    for tc in t_calls:
                        args = tc.get("args", {})
                        target_file = str(args.get("TargetFile", ""))
                        code_content = str(args.get("CodeContent", "")) or str(args.get("ReplacementContent", ""))
                        
                        if "РАБОЧИЙ_ДИАЛОГ.md" in target_file:
                            right_dialogue_chars += len(code_content)
                        else:
                            other_tools_chars += len(code_content)
            except Exception as e:
                pass
                
    left_tokens = left_chat_chars // 4
    right_tokens = right_dialogue_chars // 4
    other_tokens = other_tools_chars // 4
    total_tokens = left_tokens + right_tokens + other_tokens
    
    left_pct = round((left_tokens / total_tokens) * 100, 1) if total_tokens > 0 else 0
    right_pct = round((right_tokens / total_tokens) * 100, 1) if total_tokens > 0 else 0
    other_pct = round((other_tokens / total_tokens) * 100, 1) if total_tokens > 0 else 0
    
    return {
        "total_model_responses": total_model_responses,
        "left_chat_chars": left_chat_chars,
        "left_chat_tokens": left_tokens,
        "left_chat_pct": left_pct,
        "right_dialogue_chars": right_dialogue_chars,
        "right_dialogue_tokens": right_tokens,
        "right_dialogue_pct": right_pct,
        "other_tools_chars": other_tools_chars,
        "other_tools_tokens": other_tokens,
        "other_tools_pct": other_pct,
        "total_output_tokens": total_tokens
    }

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    res = audit_chat_silence(b_folder)
    
    print("=" * 60)
    print("📊 СРАВНИТЕЛЬНЫЙ АУДИТ РАСХОДА ЧАТОВ (chat_silence_auditor.py)")
    print("=" * 60)
    print(f"🔹 Всего откликов ИИ: {res['total_model_responses']} шагов")
    print(f"🔹 ЛЕВЫЙ ЧАТ UI (Main Window): {res['left_chat_tokens']:,} токенов ({res['left_chat_pct']}%) [{res['left_chat_chars']:,} симв]")
    print(f"🔹 ПРАВЫЙ ПУЛЬТ (РАБОЧИЙ_ДИАЛОГ.md): {res['right_dialogue_tokens']:,} токенов ({res['right_dialogue_pct']}%) [{res['right_dialogue_chars']:,} симв]")
    print(f"🔹 ДРУГИЕ ИНСТРУМЕНТЫ (Файлы ДНК/Скрипты): {res['other_tools_tokens']:,} токенов ({res['other_tools_pct']}%) [{res['other_tools_chars']:,} симв]")
    print("-" * 60)
    print(f"💡 ИТОГ ЭКОНОМИИ: Перенос аналитики в РАБОЧИЙ_ДИАЛОГ.md выгружает {res['right_dialogue_pct']}% объема без повторного выжигания чата UI!")
    print("=" * 60)
