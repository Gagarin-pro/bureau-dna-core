import os, sys, glob

STANDARD_FOOTER = """[📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md) | [🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛑 ПРАВИЛА ТЕМПА](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)"""

FILES_TO_ENFORCE = [
    os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md"),
    os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md"),
    os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md"),
    os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md"),
    os.path.join(os.path.expanduser("~"), ".gemini/config/autonomous_bureau_dashboard_master.md"),
]

CABINS_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ")
cabin_navigators = glob.glob(os.path.join(CABINS_DIR, "*/NAVIGATOR.md"))
FILES_TO_ENFORCE.extend(cabin_navigators)

def get_footer_for_file(filepath):
    if "/.gemini/antigravity/brain/" in filepath:
        folder = os.path.dirname(filepath)
        return f"[📟 ПУЛЬТ УПРАВЛЕНИЯ](file://{folder}/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file://{folder}/РАБОЧИЙ_ДИАЛОГ.md) | [🏢 АВТОНОМНОЕ БЮРО](file://{folder}/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file://{folder}/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛑 ПРАВИЛА ТЕМПА](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)"
    return STANDARD_FOOTER

def enforce_footer_in_file(filepath):
    if not os.path.exists(filepath) or not filepath.endswith(".md"):
        return False
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        lines = content.rstrip().split("\n")
        new_lines = []
        for line in lines:
            if "[🏢 АВТОНОМНОЕ БЮРО]" in line or "[📟 ПУЛЬТ УПРАВЛЕНИЯ]" in line or "[💬 ДИАЛОГ]" in line or "[👑 МАСТЕР-КАБИНА]" in line:
                continue
            new_lines.append(line)
        
        footer = get_footer_for_file(filepath)
        new_content = "\n".join(new_lines).rstrip() + "\n\n---\n\n" + footer + "\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Warning: could not enforce footer in {filepath}: {e}")
        return False

def run_footer_enforcement():
    updated_count = 0
    all_targets = list(FILES_TO_ENFORCE)
    
    brain_dir = os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain")
    if os.path.exists(brain_dir):
        for pattern in ["*/РАБОЧИЙ_ДИАЛОГ.md", "*/autonomous_bureau_dashboard.md", "*/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md", "*/ПОВЕСТКА_ПЛАНЕРКИ.md"]:
            brain_files = glob.glob(os.path.join(brain_dir, pattern))
            all_targets.extend(brain_files)

    for target in set(all_targets):
        if enforce_footer_in_file(target):
            updated_count += 1
    return updated_count

if __name__ == "__main__":
    count = run_footer_enforcement()
    print("=" * 60)
    print("🛡️ ПЕРЕСТАНОВКА 5 КНОПОК ПО ПОРЯДКУ КВС (footer_guard_enforcer.py)")
    print("=" * 60)
    print(f"🔹 Порядок зафиксирован: ПУЛЬТ ➔ ДИАЛОГ ➔ БЮРО ➔ ПЛАНЕРКА ➔ УМЕНИЯ")
    print(f"🔹 Обновлено файлов: {count}")
    print("=" * 60)
    print("🟢 ПОРЯДОК КНОПОК УСПЕШНО ПЕРЕСТАВЛЕН И ЗАПЕЧАТАН ВО ВСЕХ КАБИНАХ И СЕССИЯХ!")
    print("=" * 60)
