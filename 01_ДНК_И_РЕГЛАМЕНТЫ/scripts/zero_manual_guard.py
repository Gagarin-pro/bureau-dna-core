#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zero_manual_guard.py — Сторож Закона 100% Автономного Исполнения (Zero Manual Effort)
Анализирует выходящие диалоги на предмет попыток переложить на КВС ручную работу.
"""

import re

BANNED_MANUAL_PATTERNS = [
    r"скопируй[т]?е\s+вручную",
    r"введите\s+вручную",
    r"сделай[т]?е\s+самостоятельно",
    r"перейдите\s+в\s+консоль\s+и\s+выполните",
    r"откройте\s+терминал\s+и\s+вставьте"
]

def audit_text_for_manual_requests(text: str) -> dict:
    """Проверяет текст на наличие запрещенных предложений ручного ввода."""
    violations = []
    for pattern in BANNED_MANUAL_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            violations.extend(matches)
            
    if violations:
        return {"status": "VIOLATION", "violations": violations}
    return {"status": "GREEN_NORMAL", "violations": []}

def run_zero_manual_guard() -> dict:
    """Главный тестовый запуск сторожа автономии."""
    sample_text = "Все задачи выполняются через автономные инструменты Бюро. Ручной ввод исключен."
    return audit_text_for_manual_requests(sample_text)

if __name__ == "__main__":
    res = run_zero_manual_guard()
    print(f"🔹 [zero_manual_guard] Статус: {res['status']} | Нарушений: {len(res['violations'])}")
