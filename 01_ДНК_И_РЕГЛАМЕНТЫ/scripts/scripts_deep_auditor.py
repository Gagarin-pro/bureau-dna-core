#!/usr/bin/env python3
import os, sys, glob, py_compile

SCRIPTS_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts")

def run_deep_scripts_audit():
    script_files = glob.glob(os.path.join(SCRIPTS_DIR, "*.py"))
    audit_results = {
        "total_scripts": len(script_files),
        "valid_syntax": 0,
        "valid_utf8": 0,
        "registered_in_runner": 0,
        "details": []
    }

    runner_file = os.path.join(SCRIPTS_DIR, "unified_guards_runner.py")
    runner_content = ""
    if os.path.exists(runner_file):
        with open(runner_file, "r", encoding="utf-8") as f:
            runner_content = f.read()

    for sfile in script_files:
        bname = os.path.basename(sfile)
        item = {"filename": bname, "syntax": "OK", "utf8": "OK", "runner": "NO"}
        
        # Check syntax
        try:
            py_compile.compile(sfile, doraise=True)
            audit_results["valid_syntax"] += 1
        except Exception as e:
            item["syntax"] = f"ERROR: {e}"

        # Check UTF-8
        try:
            with open(sfile, "r", encoding="utf-8") as f:
                f.read()
            audit_results["valid_utf8"] += 1
        except Exception as e:
            item["utf8"] = f"ERROR: {e}"

        # Check if imported in unified runner
        if bname.replace(".py", "") in runner_content:
            item["runner"] = "YES"
            audit_results["registered_in_runner"] += 1

        audit_results["details"].append(item)

    return audit_results

if __name__ == "__main__":
    res = run_deep_scripts_audit()
    print("=" * 65)
    print(f"📊 ГЛУБОКИЙ АУДИТ ВСЕХ СКРИПТОВ БЮРО (С 29 ИЮНЯ ПО СЕГОДНЯ)")
    print("=" * 65)
    print(f"🔹 Всего скриптов проверено: {res['total_scripts']}")
    print(f"🔹 Валидный синтаксис: {res['valid_syntax']} / {res['total_scripts']}")
    print(f"🔹 Валидная кодировка UTF-8: {res['valid_utf8']} / {res['total_scripts']}")
    print(f"🔹 Зарегистрировано в главном моторе: {res['registered_in_runner']}")
    print("=" * 65)
    for d in res["details"]:
        status_icon = "🟢" if d["syntax"] == "OK" and d["utf8"] == "OK" else "🔴"
        print(f"{status_icon} {d['filename']} | Syntax: {d['syntax']} | UTF-8: {d['utf8']} | Runner: {d['runner']}")
    print("=" * 65)
