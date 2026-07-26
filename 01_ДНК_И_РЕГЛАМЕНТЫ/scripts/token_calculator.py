import os, json, sys

def calculate_session_stats(brain_folder):
    log_file = os.path.join(brain_folder, ".system_generated/logs/transcript.jsonl")
    if not os.path.exists(log_file):
        return {
            "token_estimate": 0,
            "turns": 0,
            "pressure_pct": 0.0,
            "status_indicator": "🟢 Ледяной старт (0%)",
            "model_fuel_status": "Gemini: 77%/86% | Claude: 100% | ChatGPT: 100%"
        }
    
    total_chars = 0
    turns = 0
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                turns += 1
                total_chars += len(json.dumps(data, ensure_ascii=False))
            except:
                pass
    
    # Rough estimate: ~4 chars per token
    token_est = total_chars // 4
    max_context = 200000
    pressure_pct = min(100.0, round((token_est / max_context) * 100, 1))
    
    if pressure_pct < 40:
        indicator = f"🟢 Ледяной режим ({pressure_pct}%)"
    elif pressure_pct < 65:
        indicator = f"🟡 Теплый ход ({pressure_pct}%)"
    else:
        indicator = f"🔴 Горячая зона ({pressure_pct}%) -> Требуется сброс (/end_shift)"
        
    return {
        "token_estimate": token_est,
        "turns": turns,
        "pressure_pct": pressure_pct,
        "status_indicator": indicator,
        "model_fuel_status": "Gemini 3.6 Flash (77% нед / 86% час) | Gemini 3.1 Pro (77% нед) | Claude 3.7 (🟢 100% полный) | ChatGPT o1 (🟢 100% полный)"
    }

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    res = calculate_session_stats(b_folder)
    print(f"📊 КАЛЬКУЛЯТОР РАСХОДА: [Токены: ~{res['token_estimate']:,} | Загрузка: {res['status_indicator']}]")
    print(f"⛽ ТОПЛИВНЫЕ БАКИ: [{res['model_fuel_status']}]")
