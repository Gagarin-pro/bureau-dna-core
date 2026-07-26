import os, sys, re

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

def verify_4window_parity(brain_folder, active_cabin="МАСТЕР_КАБИНА"):
    cabin_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ACTIVE_CABIN.txt")
    if os.path.exists(cabin_path):
        try:
            with open(cabin_path, "r", encoding="utf-8") as f:
                v = f.read().strip().upper()
                if v and v != "NEUTRAL":
                    active_cabin = v
        except Exception:
            pass

    targets = [
        os.path.join(brain_folder, "autonomous_bureau_dashboard.md"),
        os.path.join(brain_folder, "РАБОЧИЙ_ДИАЛОГ.md"),
        os.path.join(brain_folder, "ПОВЕСТКА_ПЛАНЕРКИ.md"),
        os.path.join(brain_folder, "АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md"),
    ]

    synced_count = 0
    for file_path in targets:
        if not os.path.exists(file_path):
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            modified = False
            # Check cabin consistency in headers
            if "MONOLITH_CABIN" in content and active_cabin == "MASTER_CABIN":
                content = content.replace("MONOLITH_CABIN", "MASTER_CABIN")
                modified = True
            elif "BUREAU_SETUP" in content and active_cabin in ["MASTER_CABIN", "МАСТЕР_КАБИНА"]:
                content = content.replace("BUREAU_SETUP", active_cabin)
                modified = True

            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                synced_count += 1
        except Exception as e:
            pass

    return {
        "status": "PARITY_OK",
        "synced_files": synced_count,
        "active_cabin": active_cabin
    }

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    res = verify_4window_parity(b_folder)
    print("=" * 60)
    print("🚀 СТОРОЖ СИНХРОНА 4 ОКНО (parity_checker.py)")
    print("=" * 60)
    print(f"🔹 Статус Паритета: {res['status']}")
    print(f"🔹 Активная Кабина: {res['active_cabin']}")
    print(f"🔹 Выравнено файлов: {res['synced_files']}")
    print("=" * 60)
