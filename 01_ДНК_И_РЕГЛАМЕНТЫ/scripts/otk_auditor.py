#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Сборочный автомат ОТК (Совет Мастеров / LLM Council)
Назначение: Независимый аудит сборочных чертежей и кода перед сдачей КВС.
"""

import os
import sys
import ast

def audit_python_file(fpath):
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        ast.parse(content)
        return True, "Синтаксический анализ Python пройден успешно. Ошибок компиляции ast нет."
    except SyntaxError as e:
        return False, f"Синтаксическая ошибка в строке {e.lineno}: {e.msg}\nКод: {e.text.strip() if e.text else ''}"
    except Exception as e:
        return False, f"Ошибка чтения файла: {str(e)}"

def audit_markdown_file(fpath):
    warnings = []
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for idx, line in enumerate(lines):
            # Check for bad markdown links like [`link`](file://...) which break IDE rendering
            if "[`" in line and "`](file://" in line:
                warnings.append(f"Строка {idx+1}: Обнаружена обратная кавычка внутри ссылки (ломает форматирование IDE).")
            # Check for missing file links protocol
            if "](" in line and "file://" not in line and "http" not in line and "mailto" not in line:
                # Potential relative path that should use file:// or is a broken reference
                warnings.append(f"Строка {idx+1}: Ссылка без явного протокола (file:// или http://).")
        
        if warnings:
            return False, "\n".join(warnings)
        return True, "Анализ структуры Markdown пройден успешно. Нарушений разметки не обнаружено."
    except Exception as e:
        return False, f"Ошибка чтения файла: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 otk_auditor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"🔴 ОТК: Файл не найден: {file_path}")
        sys.exit(1)

    print("--------------------------------------------------")
    print(f"⚙️ ЗАПУСК ОТК: Ревизия файла {os.path.basename(file_path)}...")
    print("--------------------------------------------------")

    ext = os.path.splitext(file_path)[1].lower()
    success = False
    report = ""

    if ext == ".py":
        success, report = audit_python_file(file_path)
    elif ext == ".md":
        success, report = audit_markdown_file(file_path)
    else:
        success, report = True, "Формат файла не требует автоматического синтаксического разбора."

    if success:
        print("🟢 ОТК: РЕЦЕНЗИЯ УСПЕШНА (Одобрено)")
        print(report)
        sys.exit(0)
    else:
        print("🔴 ОТК: ОБНАРУЖЕН БРАК (Отклонено)")
        print(report)
        sys.exit(1)

if __name__ == "__main__":
    main()
