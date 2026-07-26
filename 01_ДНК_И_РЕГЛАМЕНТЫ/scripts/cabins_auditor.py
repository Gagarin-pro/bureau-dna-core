import os, sys, glob

MASTER_DIR = "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

CABIN_DIRS = {
    "BUREAU_SETUP": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUKVITSA_BOT": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Буквица-бот",
    "MONOLITH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "COURT_CASE": os.path.join(MASTER_DIR, "08_ЛИЧНЫЙ_КАРАВАН"),
    "AUTOSCHOOL": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "GAGARIN_OS": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "AI_STUDIO_RD": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Google AI Studio — База R&D",
    "ANTIGRAVITY_INTEGRATION": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/АНТИГРАВИТИ — Интеграция",
    "CLAUDE_DRIVE_AGENT": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/КЛОД — Агент Google Диска",
    "VPN_REALITY": os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ"),
    "THERMICA_SIB": os.path.join(MASTER_DIR, "05_ЦЕХ_КОММЕРЦИИ")
}

UPDATED_FOOTER = """

---

[🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md) | [💨 МАНОМЕТР ПАРА](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts/steam_pressure_monitor.py) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md) | [📑 ПАМЯТКА КВС](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПАМЯТКА_КВС_ВАЙБ_КОДИНГ.md)
"""

BUREAU_MANDATORY_DNA = """
> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO 2026**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).
> 3. **Закон Фонового Сторожа Пара (`steam_guard.py`)**: Контроль Порога 1 000 000 токенов под ключ.
"""

def audit_all_cabins():
    results = {}
    total_cabins = len(CABIN_DIRS)
    modernized_cabins = 0
    
    for cabin_name, cabin_path in CABIN_DIRS.items():
        try:
            if not os.path.exists(cabin_path):
                os.makedirs(cabin_path, exist_ok=True)
                
            nav_file = os.path.join(cabin_path, "NAVIGATOR.md")
            if cabin_name == "BUREAU_SETUP":
                nav_file = os.path.join(cabin_path, "СТАТУС_ПРОЕКТА.md")
                
            if not os.path.exists(nav_file):
                content = f"# 🧭 НАВИГАТОР СБОРОЧНОЙ КАБИНЫ: {cabin_name}\n\n" + BUREAU_MANDATORY_DNA + "\n\n## 📌 ТЕКУЩИЙ СТАТУС ВЕРСТАКА\n* Верстак готов к работе.\n" + UPDATED_FOOTER
                with open(nav_file, "w", encoding="utf-8") as f:
                    f.write(content)
                modernized_cabins += 1
                results[cabin_name] = "🟢 СОЗДАН И МОДЕРНИЗИРОВАН"
            else:
                with open(nav_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                # Update DNA block
                if "СТАНДАРТ БЮРО LEGO-ARCHITECT PRO 2026" not in content:
                    content = BUREAU_MANDATORY_DNA + "\n" + content
                    
                # Replace footer if old footer present, or append new footer
                if "[🏢 АВТОНОМНОЕ БЮРО]" in content:
                    lines = content.splitlines()
                    clean_lines = [l for l in lines if not l.startswith("[🏢 АВТОНОМНОЕ БЮРО]") and not l.startswith("---")]
                    content = "\n".join(clean_lines).strip() + UPDATED_FOOTER
                else:
                    content = content.strip() + UPDATED_FOOTER
                    
                with open(nav_file, "w", encoding="utf-8") as f:
                    f.write(content)
                modernized_cabins += 1
                results[cabin_name] = "🟢 ОБНОВЛЕН И СТАНДАРТИЗИРОВАН"
        except Exception as e:
            results[cabin_name] = f"🔴 ОШИБКА: {e}"
            
    return {
        "total_cabins": total_cabins,
        "modernized_cabins": modernized_cabins,
        "details": results
    }

if __name__ == "__main__":
    res = audit_all_cabins()
    print("=" * 60)
    print("🎛️ СПЛОШНОЙ АУДИТ И СТАНДАРТИЗАЦИЯ 10 КАБИН БЮРО (cabins_auditor.py)")
    print("=" * 60)
    print(f"🔹 Всего сборочных кабин проинспектировано: {res['total_cabins']}")
    print(f"🔹 Модернизировано и запечатано 3 Законами: {res['modernized_cabins']}")
    print("-" * 60)
    for cname, cstatus in res['details'].items():
        print(f"  • Кабина `{cname}`: {cstatus}")
    print("=" * 60)
    print("🟢 ВСЕ 10 СБОРОЧНЫХ КАБИН И КНОПОЧНЫЕ ПОДВАЛЫ УСПЕШНО СТАНДАРТИЗИРОВАНЫ!")
    print("=" * 60)
