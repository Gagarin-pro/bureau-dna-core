#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Когнитивный Навигатор Фокуса»
Назначение: Анализ сменного журнала, предотвращение отклонений от утвержденного плана и контроль дрейфа внимания.
"""

import os
import re

def parse_shift_log(log_path):
    plan_tasks = []
    current_status = []
    
    if not os.path.exists(log_path):
        return None
        
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Парсим Стартовый план
    plan_section = re.search(r'## 📋 СТАРТОВЫЙ ПЛАН РАБОЧЕГО ДНЯ.*?(?=##|$)', content, re.DOTALL)
    if plan_section:
        tasks = re.findall(r'(\d+)\.\s+`\[(.*?)\]`\s+(.*?)(?=\n\d+\.|\n\n|\n---|$)', plan_section.group(0), re.DOTALL)
        for t in tasks:
            plan_tasks.append({
                "num": t[0],
                "status": t[1].strip(),
                "text": t[2].strip()
            })
            
    # Парсим Текущий статус выполнения
    status_section = re.search(r'## 📈 ТЕКУЩИЙ СТАТУС ВЫПОЛНЕНИЯ.*?(?=---|$)', content, re.DOTALL)
    if status_section:
        logs = re.findall(r'\*\s+\*\*(\d{2}:\d{2})\*\*\s+—\s+(.*?)(?=\n\*|\n\n|$)', status_section.group(0), re.DOTALL)
        for l in logs:
            current_status.append({
                "time": l[0],
                "text": l[1].strip()
            })
            
    return plan_tasks, current_status

def audit_focus(workspace_root):
    log_path = os.path.join(workspace_root, "03_БОРТОВОЙ_КАРАВАН/СМЕННЫЙ_ЖУРНАЛ.md")
    parsed = parse_shift_log(log_path)
    
    if not parsed:
        print("🔴 ОШИБКА НАВИГАЦИИ: Сменный журнал не найден по адресу.")
        return
        
    plan_tasks, current_status = parsed
    
    print("=======================================================")
    print("🧭 КОГНИТИВНЫЙ РАДАР ИИ-НАВИГАТОРА (FOCUS TELEMETRY)")
    print("=======================================================")
    
    # 1. Анализируем TODO-лист
    open_tasks = [t for t in plan_tasks if t["status"] != "x"]
    closed_tasks = [t for t in plan_tasks if t["status"] == "x"]
    
    print(f"📊 Статус выполнения плана: {len(closed_tasks)} / {len(plan_tasks)} завершено.")
    
    if open_tasks:
        print("\n🚀 ОЧЕРЕДЬ СЛЕДУЮЩИХ ЗАДАЧ (PLAN QUEUE):")
        for t in open_tasks:
            clean_text = re.sub(r'\s+', ' ', t["text"])
            print(f"  [ ] Шаг {t['num']}: {clean_text}")
    else:
        print("\n🎉 ВСЕ ЗАДАЧИ ИЗ СТАРТОВОГО ПЛАНА ВЫПОЛНЕНЫ!")
        
    # 2. Проверяем наличие отклонений
    print("\n⏱️ ПОСЛЕДНЯЯ ЗАФИКСИРОВАННАЯ ОПЕРАЦИЯ:")
    if current_status:
        last_op = current_status[-1]
        print(f"  🕒 {last_op['time']} — {last_op['text']}")
    else:
        print("  ⚠️ Нет записей в хронологическом журнале.")
        
    # 3. Рекомендация Навигатора
    print("\n💡 РЕКОМЕНДАЦИЯ НАВИГАТОРА:")
    if open_tasks:
        next_task = open_tasks[0]
        print(f"  🟢 Следующий приоритетный курс: Шаг {next_task['num']} -> {next_task['text']}")
    else:
        print("  🟢 Смена полностью отработана. Рекомендуется выполнить Протокол Закрытия (Раздел 14).")
    print("=======================================================")

if __name__ == "__main__":
    # Находим корень проекта (на уровень выше от папки скриптов)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    audit_focus(project_root)
