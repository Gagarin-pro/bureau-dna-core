#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «ОТК-Валидатор Кода»
Назначение: Автоматическая проверка синтаксиса Python и JavaScript файлов перед коммитом и деплоем.
"""

import os
import subprocess
import sys

def validate_python(file_path):
    try:
        res = subprocess.run([sys.executable, "-m", "py_compile", file_path], capture_output=True, text=True)
        if res.returncode == 0:
            return True, "🟢 OK"
        else:
            return False, f"🔴 Ошибка компиляции:\n{res.stderr.strip()}"
    except Exception as e:
        return False, f"🔴 Ошибка запуска компилятора: {str(e)}"

def validate_javascript(file_path):
    try:
        # Проверяем синтаксис JS с помощью встроенной команды node --check
        res = subprocess.run(["node", "--check", file_path], capture_output=True, text=True)
        if res.returncode == 0:
            return True, "🟢 OK"
        else:
            return False, f"🔴 Ошибка синтаксиса JS:\n{res.stderr.strip()}"
    except FileNotFoundError:
        return True, "🟡 Пропущено (Node.js не установлен на хосте)"
    except Exception as e:
        return False, f"🔴 Ошибка запуска node: {str(e)}"

def run_otk_validation(project_root):
    print("=======================================================")
    print("🔍 СТЕНД ОТК-ВАЛИДАЦИИ КОДА (CODE QA AUDIT)")
    print("=======================================================")
    
    has_errors = False
    
    # Рекурсивно сканируем цеха
    for root, dirs, files in os.walk(project_root):
        # Игнорируем виртуальные окружения и скрытые папки
        if any(ignored in root for ignored in [".git", "venv", ".venv", "node_modules", ".tempmediaStorage"]):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_root)
            
            # Проверяем Python
            if file.endswith(".py"):
                ok, msg = validate_python(file_path)
                print(f"🐍 Python: {rel_path} -> {msg}")
                if not ok:
                    has_errors = True
                    
            # Проверяем JavaScript
            elif file.endswith(".js"):
                ok, msg = validate_javascript(file_path)
                print(f"⚡ JS: {rel_path} -> {msg}")
                if not ok:
                    has_errors = True
                    
    print("=======================================================")
    if has_errors:
        print("🔴 ВНИМАНИЕ: Обнаружен брак! См. отчет выше. Коррекция обязательна.")
        return False
    else:
        print("🟢 ОТК пройден. Все сборочные единицы соответствуют синтаксическим стандартам.")
        return True

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    
    success = run_otk_validation(project_root)
    sys.exit(0 if success else 1)
