#!/usr/bin/env python3
import os, sys, shutil, datetime

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

CABIN_DIRS = {
    "МАСТЕР_КАБИНА": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUREAU_SETUP": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUKVITSA_BOT": os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Буквица-бот",
    "MONOLITH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "MONOLITH_CEH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "COURT_CASE": os.path.join(MASTER_DIR, "08_ЛИЧНЫЙ_КАРАВАН"),
    "AUTOSCHOOL": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "GAGARIN_OS": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "AI_STUDIO_RD": os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Google AI Studio — База R&D",
    "VPN_REALITY": os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ"),
}

def sync_and_archive_agenda(brain_folder, active_cabin="МАСТЕР_КАБИНА"):
    cabin_dir = CABIN_DIRS.get(active_cabin, os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"))
    agendas_dir = os.path.join(cabin_dir, "ПЛАНЕРКИ")
    os.makedirs(agendas_dir, exist_ok=True)

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    current_agenda = os.path.join(brain_folder, "ПОВЕСТКА_ПЛАНЕРКИ.md")
    master_agenda = os.path.join(cabin_dir, "ПОВЕСТКА_ПЛАНЕРКИ.md")

    # 1. Sync from brain to master cabin folder if exists
    if os.path.exists(current_agenda):
        shutil.copy2(current_agenda, master_agenda)
        daily_archive = os.path.join(agendas_dir, f"{today_str}_ПОВЕСТКА_ПЛАНЕРКИ.md")
        shutil.copy2(current_agenda, daily_archive)
    elif os.path.exists(master_agenda):
        shutil.copy2(master_agenda, current_agenda)
        daily_archive = os.path.join(agendas_dir, f"{today_str}_ПОВЕСТКА_ПЛАНЕРКИ.md")
        shutil.copy2(master_agenda, daily_archive)

    return {
        "active_cabin": active_cabin,
        "cabin_dir": cabin_dir,
        "today_agenda_archive": os.path.join(agendas_dir, f"{today_str}_ПОВЕСТКА_ПЛАНЕРКИ.md")
    }

if __name__ == "__main__":
    brain = sys.argv[1] if len(sys.argv) > 1 else None
    cabin = sys.argv[2] if len(sys.argv) > 2 else "МАСТЕР_КАБИНА"
    res = sync_and_archive_agenda(brain, cabin)
    print("=" * 60)
    print("📅 АВТО-СИНХРОНИЗАЦИЯ И ДНЕВНОЙ АРХИВ ПОВЕСТКИ (agenda_auto_sync.py)")
    print("=" * 60)
    print(f"🔹 Активная кабина: {res['active_cabin']}")
    print(f"🔹 Архив повестки за сегодня: {res['today_agenda_archive']}")
    print("=" * 60)
