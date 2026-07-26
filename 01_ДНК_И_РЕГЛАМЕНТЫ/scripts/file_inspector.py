#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Смотритель порядка»
Назначение: Автоматическая очистка и упорядочивание файлов на Google Диске и Рабочем столе
"""

import os
import shutil
import glob

def get_paths():
    home = os.path.expanduser("~")
    # Base Google Drive root
    gd_root = os.path.join(home, "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии")
    
    paths = {
        "gd_root": gd_root,
        "desktop": os.path.join(home, "Desktop"),
        "monolith_dest": os.path.join(gd_root, "AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/06_ЦЕХ_МОНОЛИТ/документы"),
        "vpn_dest": os.path.join(gd_root, "AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/02_ЦЕХ_ГАГАРИН/архив_vpn"),
        "ai_studio_dest": os.path.join(gd_root, "AI_Studio/Google AI Studio — База R&D"),
        "concept_dest": os.path.join(gd_root, "AI_Studio/Автошкола ИИ/01_Концепции_и_Стратегии_Школы_ИИ"),
        "dialogs_dest": os.path.join(gd_root, "AI_Studio/Google AI Studio — База R&D/ИИ диалоги")
    }
    return paths

def safe_move(src, dest_dir):
    if not os.path.exists(src):
        return False
    
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(src))
    
    # Avoid overwriting
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(os.path.basename(src))
        counter = 1
        while os.path.exists(os.path.join(dest_dir, f"{base}_{counter}{ext}")):
            counter += 1
        dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
        
    try:
        shutil.move(src, dest_path)
        print(f"[+] Перемещено: {os.path.basename(src)} -> {dest_dir}")
        return True
    except Exception as e:
        print(f"[-] Ошибка перемещения {src}: {e}")
        return False

def clean_empty_dir(path):
    if os.path.exists(path) and os.path.isdir(path):
        # Ignore system files like .DS_Store
        files = [f for f in os.listdir(path) if f != ".DS_Store"]
        if not files:
            try:
                shutil.rmtree(path)
                print(f"[+] Удалена пустая папка: {os.path.basename(path)}")
            except Exception as e:
                print(f"[-] Не удалось удалить {path}: {e}")

def run_inspector():
    paths = get_paths()
    print("🧹 Запуск инспекции порядка в цехах...")
    
    # 1. Сортировка файлов Монолита
    monolith_source_dir = os.path.join(paths["gd_root"], "Монолит")
    if os.path.exists(monolith_source_dir):
        for f in glob.glob(os.path.join(monolith_source_dir, "*")):
            if os.path.basename(f) != ".DS_Store":
                safe_move(f, paths["monolith_dest"])
        clean_empty_dir(monolith_source_dir)

    # 2. Сортировка файлов VPN
    vpn_source_dir = os.path.join(paths["gd_root"], "VPN")
    if os.path.exists(vpn_source_dir):
        for f in glob.glob(os.path.join(vpn_source_dir, "*")):
            if os.path.basename(f) != ".DS_Store":
                safe_move(f, paths["vpn_dest"])
        clean_empty_dir(vpn_source_dir)

    # 3. Устранение дубликата Google Al studio (с опечаткой Al)
    google_al_studio = os.path.join(paths["gd_root"], "AI_Studio/Google Al studio")
    if os.path.exists(google_al_studio):
        for f in glob.glob(os.path.join(google_al_studio, "*")):
            if os.path.basename(f) != ".DS_Store":
                safe_move(f, paths["ai_studio_dest"])
        clean_empty_dir(google_al_studio)

    # 4. Сортировка ИИ диалогов
    dialogs_source = os.path.join(paths["gd_root"], "ИИ диалоги ")
    if os.path.exists(dialogs_source):
        # Move directory contents to dialogs_dest
        for f in glob.glob(os.path.join(dialogs_source, "*")):
            if os.path.basename(f) != ".DS_Store":
                safe_move(f, paths["dialogs_dest"])
        clean_empty_dir(dialogs_source)

    # 5. Сортировка Доходов в интернете
    income_source = os.path.join(paths["gd_root"], "Доход в интернете ")
    if os.path.exists(income_source):
        for f in glob.glob(os.path.join(income_source, "*")):
            if os.path.basename(f) != ".DS_Store":
                safe_move(f, paths["concept_dest"])
        clean_empty_dir(income_source)

    print("✨ Инспекция порядка успешно завершена.")

if __name__ == "__main__":
    run_inspector()
