import os, sys, json, glob

def monitor_steam_pressure(brain_folder):
    log_file = os.path.join(brain_folder, ".system_generated/logs/transcript_full.jsonl")
    if not os.path.exists(log_file):
        log_file = os.path.join(brain_folder, ".system_generated/logs/transcript.jsonl")
        
    if not os.path.exists(log_file):
        return {
            "tokens": 0,
            "pct": 0.0,
            "zone": "🟢 Ледяной режим",
            "action": "Штатная работа"
        }
        
    log_size = os.path.getsize(log_file)
    # Estimate tokens from physical log bytes
    tokens = log_size // 4
    
    # Gemini 3.6 Flash max context limit = 2,000,000 tokens
    max_context = 2000000
    pct = round((tokens / max_context) * 100, 1)
    
    if tokens < 300000:
        zone = "🟢 Ледяной режим"
        action = "Полная свобода, максимальный КПД"
    elif tokens < 700000:
        zone = "🟢 Комфортная смена"
        action = "Штатная работа в обычном режиме"
    elif tokens < 1000000:
        zone = "🟧 Предупредительная зона"
        action = "Подготовка Переходного Моста"
    else:
        zone = "🔴 КРАСНАЯ ЗОНА ПЕРЕХОДА"
        action = "ПОРОГ ПЕРЕХОДА: Создание TRANSITION_BRIDGE.md и переключение"
        
    return {
        "log_bytes": log_size,
        "tokens": tokens,
        "pct": pct,
        "max_context": max_context,
        "zone": zone,
        "action": action
    }

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    res = monitor_steam_pressure(b_folder)
    print("=" * 60)
    print("💨 МОНИТОР ДАВЛЕНИЯ ПАРА СЕССИИ (steam_pressure_monitor.py)")
    print("=" * 60)
    print(f"🔹 Физический размер лога смены: {res['log_bytes']:,} байт")
    print(f"🔹 Живой объем пара в токенах: ~{res['tokens']:,} токенов ({res['pct']}% от 2M бака Gemini)")
    print(f"🔹 Зона состояния котлов: {res['zone']}")
    print(f"🔹 Рекомендуемое действие: {res['action']}")
    print("=" * 60)
