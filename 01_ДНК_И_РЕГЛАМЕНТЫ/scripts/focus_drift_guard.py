#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
focus_drift_guard.py — Сторож Закона Твердого Штурмана Фокуса (Ошибка №5)
Автоматически проверяет Повестку Планерки на наличие открытых незавершенных тем.
"""

import os
import re

def audit_agenda_focus(agenda_path: str) -> dict:
    """Анализирует повестку планерки и возвращает статус активности тем."""
    if not os.path.exists(agenda_path):
        return {"status": "ERROR", "reason": "Agenda file not found"}
    
    with open(agenda_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    active_topics = re.findall(r'(\d+)\.\s*🟢\s*\*\*ТЕМА\s*№(\d+)\s*\(([^)]+)\)\:\*\*\s*(.*)', content)
    paused_topics = re.findall(r'(\d+)\.\s*⏸️\s*\*\*ТЕМА\s*№(\d+)\s*\(([^)]+)\)\:\*\*\s*(.*)', content)
    completed_topics = re.findall(r'(\d+)\.\s*✅\s*\*\*ТЕМА\s*№(\d+)\s*\(([^)]+)\)\:\*\*\s*(.*)', content)
    
    return {
        "status": "GREEN_NORMAL",
        "active_count": len(active_topics),
        "paused_count": len(paused_topics),
        "completed_count": len(completed_topics),
        "active_topics": [t[1] for t in active_topics]
    }

def run_focus_drift_guard(agenda_path: str = None) -> dict:
    """Главная точка входа сторожа фокуса."""
    if not agenda_path:
        agenda_path = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md")
    return audit_agenda_focus(agenda_path)

if __name__ == "__main__":
    res = run_focus_drift_guard()
    print(f"🔹 [focus_drift_guard] Статус: {res['status']} | Активных тем: {res['active_count']} | Завершенных тем: {res['completed_count']}")
