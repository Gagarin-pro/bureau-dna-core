import os, json, sys

def audit_shift_fuel(brain_folder, weekly_burned_pct=1.0, hourly_burned_pct=10.0):
    log_file = os.path.join(brain_folder, ".system_generated/logs/transcript.jsonl")
    if not os.path.exists(log_file):
        return {"error": f"Log file not found: {log_file}"}
    
    total_turns = 0
    user_msgs = 0
    model_resps = 0
    user_chars = 0
    model_chars = 0
    tool_calls_count = 0
    tool_breakdown = {}
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                total_turns += 1
                step_type = data.get("type", "")
                
                if step_type == "USER_INPUT":
                    user_msgs += 1
                    content = str(data.get("content", ""))
                    user_chars += len(content)
                elif step_type == "PLANNER_RESPONSE":
                    model_resps += 1
                    content = str(data.get("content", ""))
                    model_chars += len(content)
                    
                    t_calls = data.get("tool_calls", [])
                    if t_calls:
                        for tc in t_calls:
                            tool_calls_count += 1
                            t_name = tc.get("name", "unknown")
                            tool_breakdown[t_name] = tool_breakdown.get(t_name, 0) + 1
            except Exception as e:
                pass
                
    total_chars = user_chars + model_chars
    total_tokens = total_chars // 4
    
    tokens_per_hourly_pct = round(total_tokens / hourly_burned_pct, 1) if hourly_burned_pct > 0 else 0
    tokens_per_weekly_pct = round(total_tokens / weekly_burned_pct, 1) if weekly_burned_pct > 0 else 0
    avg_tokens_per_turn = round(total_tokens / model_resps, 1) if model_resps > 0 else 0
    
    report = {
        "total_turns": total_turns,
        "user_messages": user_msgs,
        "model_responses": model_resps,
        "user_chars": user_chars,
        "model_chars": model_chars,
        "total_chars": total_chars,
        "total_tokens_est": total_tokens,
        "tool_calls_count": tool_calls_count,
        "tool_breakdown": tool_breakdown,
        "hourly_burned_pct": hourly_burned_pct,
        "weekly_burned_pct": weekly_burned_pct,
        "tokens_per_hourly_pct": tokens_per_hourly_pct,
        "tokens_per_weekly_pct": tokens_per_weekly_pct,
        "avg_tokens_per_turn": avg_tokens_per_turn,
        "pct_hourly_per_turn": round((avg_tokens_per_turn / tokens_per_hourly_pct), 2) if tokens_per_hourly_pct > 0 else 0
    }
    return report

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    rep = audit_shift_fuel(b_folder, weekly_burned_pct=1.0, hourly_burned_pct=10.0)
    
    print("=" * 60)
    print("📊 МАТЕМАТИЧЕСКИЙ АУДИТ РАСХОДА ТОПЛИВА СМЕНИ (shift_fuel_auditor.py)")
    print("=" * 60)
    print(f"🔹 Всего шагов траектории: {rep['total_turns']} записей")
    print(f"🔹 Шагов ИИ: {rep['model_responses']} ответов ИИ ({rep['user_messages']} запросов КВС)")
    print(f"🔹 Символов обработано: {rep['total_chars']:,} симв ({rep['user_chars']:,} ввод / {rep['model_chars']:,} вывод)")
    print(f"🔹 Оценка объема токенов: ~{rep['total_tokens_est']:,} токенов")
    print(f"🔹 Вызовов инструментов: {rep['tool_calls_count']} операций {rep['tool_breakdown']}")
    print("-" * 60)
    print("⛽ СОПОСТАВЛЕНИЕ С ЛИМИТАМИ СТЕНДА GEMINI (86% час / 77% нед):")
    print(f"🔻 Списано часового лимита: {rep['hourly_burned_pct']}% (1% часового бака = ~{rep['tokens_per_hourly_pct']:,} токенов)")
    print(f"🔻 Списано недельного лимита: {rep['weekly_burned_pct']}% (1% недельного бака = ~{rep['tokens_per_weekly_pct']:,} токенов)")
    print(f"🎯 Средняя цена 1 ответа ИИ с инструментами: ~{rep['avg_tokens_per_turn']:,} токенов (~{rep['pct_hourly_per_turn']}% часового бака)")
    print("=" * 60)
