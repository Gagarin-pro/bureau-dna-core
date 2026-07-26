#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Бортовой Архивариус»
Назначение: Автоматизация версионирования (Git-точки сохранения) на каждом такте сборочных работ.
"""

import os
import subprocess

def init_git_repo(project_root):
    # 1. Проверяем инициализацию репозитория
    git_dir = os.path.join(project_root, ".git")
    if not os.path.exists(git_dir):
        print("📁 Инициализация локального Git-хранилища...")
        subprocess.run(["git", "init"], cwd=project_root)
        
    # 2. Создаем .gitignore если отсутствует
    gitignore_path = os.path.join(project_root, ".gitignore")
    if not os.path.exists(gitignore_path):
        print("📄 Создание системного фильтра .gitignore...")
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("# 🧱 CONSTRUCTOR-ARCHITECT PRO — GIT IGNORE FILTERS\n")
            f.write(".DS_Store\n")
            f.write("*.gdoc\n")
            f.write("*.bak\n")
            f.write("*.log\n")
            f.write(".venv/\n")
            f.write("venv/\n")
            f.write("node_modules/\n")
            f.write("dist/\n")
            f.write(".tempmediaStorage/\n")

def commit_checkpoint(project_root, message):
    init_git_repo(project_root)
    
    # Добавляем все изменения
    subprocess.run(["git", "add", "."], cwd=project_root)
    
    # Проверяем, есть ли изменения для коммита
    status = subprocess.run(["git", "status", "--porcelain"], cwd=project_root, capture_output=True, text=True)
    if not status.stdout.strip():
        print("🟢 Нет измененных кубиков для создания точки сохранения.")
        return
        
    # Создаем коммит
    print(f"💾 Создание точки сохранения: \"{message}\"")
    result = subprocess.run(["git", "commit", "-m", message], cwd=project_root, capture_output=True, text=True)
    
    # Выводим краткий итог коммита
    lines = result.stdout.strip().split('\n')
    if lines:
        print(f"  ✅ {lines[0]}")
        if len(lines) > 1:
            print(f"  📊 {lines[-1]}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    
    # В качестве сообщения берем дефолтное или из аргументов
    import sys
    msg = "Автоматическая точка сохранения ИИ-Архитектора"
    if len(sys.argv) > 1:
        msg = sys.argv[1]
        
    commit_checkpoint(project_root, msg)
