#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_pack_builder.py — Автоматический упаковщик бортового аудиторского пакета (Шаг 2 Темы #103)
Собирает все кодовые ДНК, скрипты, умения и прицепы памяти с 29 июня 2026 года в единый ZIP-архив.
"""

import os
import sys
import zipfile

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"
SKILLS_DIR = os.path.join(os.path.expanduser("~"), ".gemini/config/plugins/lego-architect-plugin/skills"
DESKTOP_OUTPUT_ZIP = os.path.join(os.path.expanduser("~"), "Desktop/BUREAU_FULL_AUDIT_PACK_2026.zip"
DRIVE_OUTPUT_ZIP = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/BUREAU_FULL_AUDIT_PACK_2026.zip")

def build_audit_package() -> dict:
    """Формирует сжатый аудиторский архив для Google Jules и AI Studio."""
    files_to_pack = []
    
    # 1. ДНК и Скрипты
    dna_dir = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ")
    if os.path.exists(dna_dir):
        for root, _, files in os.walk(dna_dir):
            for file in files:
                if not file.startswith('.') and not file.endswith('.pyc') and '__pycache__' not in root:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, MASTER_DIR)
                    files_to_pack.append((full_path, rel_path))

    # 2. Бортовой караван и памяти
    caravan_dir = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН")
    if os.path.exists(caravan_dir):
        for root, _, files in os.walk(caravan_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, MASTER_DIR)
                    files_to_pack.append((full_path, rel_path))

    # 3. Картотека Умений (Skills)
    if os.path.exists(SKILLS_DIR):
        for root, _, files in os.walk(SKILLS_DIR):
            for file in files:
                if file == 'SKILL.md' or file.endswith('.py') or file.endswith('.sh'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.join("skills", os.path.relpath(full_path, SKILLS_DIR))
                    files_to_pack.append((full_path, rel_path))

    # Создание ZIP на Desktop
    os.makedirs(os.path.dirname(DESKTOP_OUTPUT_ZIP), exist_ok=True)
    with zipfile.ZipFile(DESKTOP_OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for full_p, rel_p in files_to_pack:
            zf.write(full_p, rel_p)

    # Копирование на Google Диск
    import shutil
    shutil.copy2(DESKTOP_OUTPUT_ZIP, DRIVE_OUTPUT_ZIP)

    zip_size_kb = round(os.path.getsize(DESKTOP_OUTPUT_ZIP) / 1024, 2)
    return {
        "status": "GREEN_NORMAL",
        "packed_files_count": len(files_to_pack),
        "zip_size_kb": zip_size_kb,
        "desktop_path": DESKTOP_OUTPUT_ZIP,
        "drive_path": DRIVE_OUTPUT_ZIP
    }

if __name__ == "__main__":
    res = build_audit_package()
    print(f"🔹 [audit_pack_builder] Успешно! Запаковано файлов: {res['packed_files_count']} | Размер: {res['zip_size_kb']} KB")
