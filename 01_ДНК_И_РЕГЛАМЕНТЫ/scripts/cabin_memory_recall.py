#!/usr/bin/env python3
import os, sys, shutil, datetime, glob

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»")

CABIN_DIRS = {
    "МАСТЕР_КАБИНА": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUREAU_SETUP": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUKVITSA_BOT": os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Буквица-бот"),
    "MONOLITH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "MONOLITH_CEH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "COURT_CASE": os.path.join(MASTER_DIR, "08_ЛИЧНЫЙ_КАРАВАН"),
    "AUTOSCHOOL": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "GAGARIN_OS": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "AI_STUDIO_RD": os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Google AI Studio — База R&D"),
    "VPN_REALITY": os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ"),
}

def archive_and_recall_cabin_memory(brain_folder, active_cabin="МАСТЕР_КАБИНА", target_date=None):
    cabin_dir = CABIN_DIRS.get(active_cabin, os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"))
    dialogs_dir = os.path.join(cabin_dir, "ДИАЛОГИ")
    os.makedirs(dialogs_dir, exist_ok=True)

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    current_dialog = os.path.join(brain_folder, "РАБОЧИЙ_ДИАЛОГ.md")

    if os.path.exists(current_dialog):
        daily_archive_path = os.path.join(dialogs_dir, f"{today_str}_РАБОЧИЙ_ДИАЛОГ.md")
        shutil.copy2(current_dialog, daily_archive_path)

    archives = sorted(glob.glob(os.path.join(dialogs_dir, "*_РАБОЧИЙ_ДИАЛОГ.md")))
    
    selected_archive = None
    if target_date:
        for a in archives:
            if target_date in a:
                selected_archive = a
                break
    else:
        for a in reversed(archives):
            if not a.endswith(f"{today_str}_РАБОЧИЙ_ДИАЛОГ.md"):
                selected_archive = a
                break

    archive_content = None
    if selected_archive and os.path.exists(selected_archive):
        with open(selected_archive, "r", encoding="utf-8", errors="ignore") as f:
            archive_content = f.read()

    return {
        "active_cabin": active_cabin,
        "cabin_dir": cabin_dir,
        "today_archive": os.path.join(dialogs_dir, f"{today_str}_РАБОЧИЙ_ДИАЛОГ.md"),
        "selected_archive": selected_archive,
        "total_daily_archives": len(archives),
        "archive_content": archive_content
    }

if __name__ == "__main__":
    brain = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain/92f3f6f7-7f47-44fc-92e9-0ee82cb9e441")
    cabin = sys.argv[2] if len(sys.argv) > 2 else "МАСТЕР_КАБИНА"
    tdate = sys.argv[3] if len(sys.argv) > 3 else "2026-07-24"
    res = archive_and_recall_cabin_memory(brain, cabin, tdate)
    print("=" * 60)
    print("🧠 АВТО-ПАМЯТЬ И ДНЕВНОЙ АРХИВ КАБИНЫ (cabin_memory_recall.py)")
    print("=" * 60)
    print(f"🔹 Активная кабина: {res['active_cabin']}")
    print(f"🔹 Выбранный архив памяти: {res['selected_archive']}")
    print(f"🔹 Всего дневных архивов: {res['total_daily_archives']}")
    print("=" * 60)
    if res['archive_content']:
        print("📄 СОДЕРЖИМОЕ АРХИВА:")
        print(res['archive_content'][:600])
        print("...")
