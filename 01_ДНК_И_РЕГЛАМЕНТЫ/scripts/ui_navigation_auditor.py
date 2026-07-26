#!/usr/bin/env python3
import os, sys, re, glob

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

def audit_ui_navigation_links(brain_folder=None):
    files_to_check = [
        os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md"),
        os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md"),
        os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md"),
        os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md"),
        os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md"),
    ]
    if brain_folder and os.path.exists(brain_folder):
        for bfile in ["autonomous_bureau_dashboard.md", "РАБОЧИЙ_ДИАЛОГ.md", "ПОВЕСТКА_ПЛАНЕРКИ.md"]:
            bfpath = os.path.join(brain_folder, bfile)
            if os.path.exists(bfpath):
                files_to_check.append(bfpath)

    results = {
        "status": "GREEN",
        "total_links_found": 0,
        "valid_links": 0,
        "broken_links": 0,
        "details": []
    }

    link_pattern = re.compile(r'\[([^\]]+)\]\((file://[^\)]+)\)')

    for fpath in files_to_check:
        if not os.path.exists(fpath):
            continue
        bname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        matches = link_pattern.findall(content)
        for label, uri in matches:
            results["total_links_found"] += 1
            clean_path = uri.replace("file://", "").split("#")[0]
            clean_path = clean_path.replace("%20", " ")
            
            if os.path.exists(clean_path):
                results["valid_links"] += 1
            else:
                results["broken_links"] += 1
                results["status"] = "RED"
                results["details"].append(f"🔴 Битая ссылка '{label}' в {bname} -> {clean_path}")

    return results

if __name__ == "__main__":
    res = audit_ui_navigation_links()
    print("=" * 65)
    print("🖥️  АУДИТ КНОПОК И ССЫЛОК ПАНЕЛИ УПРАВЛЕНИЯ (ui_navigation_auditor.py)")
    print("=" * 65)
    print(f"🔹 Статус: {res['status']}")
    print(f"🔹 Всего ссылок найдено: {res['total_links_found']}")
    print(f"🔹 Валидные физические пути: {res['valid_links']} / {res['total_links_found']}")
    print(f"🔹 Битые ссылки: {res['broken_links']}")
    print("=" * 65)
    for d in res["details"]:
        print(d)
