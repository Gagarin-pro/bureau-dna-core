#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Штурман-Исследователь»
Назначение: Фильтрация устаревших технологий (legacy) и автогенерация оптимальных поисковых шаблонов.
"""

import sys

# База данных устаревших костылей (Legacy) и их современных нативных альтернатив
LEGACY_FILTERS = {
    "howler": "Native Web Audio API (нативный синтез и проигрывание звука)",
    "soundjs": "Native Web Audio API",
    "jquery": "Native DOM (document.querySelector, document.querySelectorAll)",
    "moment": "Native Date или Intl API (в будущем Temporal)",
    "axios": "Native fetch() API",
    "lodash": "Native ES6+ Array/Object methods (map, filter, reduce, etc.)",
    "crypto-js": "Native Web Crypto API (crypto.subtle)",
    "swal": "Native <dialog> element (модальные окна в HTML5)"
}

def analyze_tech_stack(query):
    query_lower = query.lower()
    warnings = []
    
    # 1. Проверяем наличие устаревших библиотек в запросе
    for legacy, modern in LEGACY_FILTERS.items():
        if legacy in query_lower:
            warnings.append(f"⚠️  ОБНАРУЖЕН УСТАРЕВШИЙ КОСТЫЛЬ: [{legacy}]\n    👉 Рекомендация: Используйте {modern} для максимальной легкости и скорости.")
            
    print("=======================================================")
    print("🧭 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ ТЕХНОЛОГИЙ (TECH SCOUT)")
    print("=======================================================")
    print(f"🔍 Запрос: \"{query}\"\n")
    
    if warnings:
        for w in warnings:
            print(w)
            print()
    else:
        print("🟢 Запрос чист от известных устаревших библиотек.")
        
    # 2. Формируем оптимальный поисковый промпт для Perplexity Pro
    print("📋 ОПТИМАЛЬНЫЙ ШАБЛОН ДЛЯ ПОИСКА В PERPLEXITY PRO:")
    perplexity_prompt = (
        f"\"Используй только современные стандарты ES6+, CSS3 и HTML5. "
        f"Найди самое легкое, быстрое и современное решение без лишних внешних библиотек для: {query}\""
    )
    print(f"  {perplexity_prompt}")
    print("=======================================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 web_scout.py \"[описание задачи или технологии]\"")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    analyze_tech_stack(query)
