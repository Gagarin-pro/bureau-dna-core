#!/usr/bin/env python3
import os, sys, shutil, datetime

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"
CARAVAN_DIR = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН")

def pack_bridge_for_new_chat(brain_folder, active_topic="Единая Настройка Мастер-Кабины V3.0", entry_cube="Продолжение смены по наряду КВС"):
    bridge_path_brain = os.path.join(brain_folder, "ПЕРЕХОДНЫЙ_МОСТ.md")
    bridge_path_caravan = os.path.join(CARAVAN_DIR, "ПЕРЕХОДНЫЙ_МОСТ.md")
    
    today_str = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    
    content = f"""# 🌉 ПЕРЕХОДНЫЙ МОСТ БЮРО — МАСТЕР_КАБИНА V3.0
> **Дата упаковки моста:** {today_str} | **Статус:** 🟢 ГОТОВ К МГНОВЕННОМУ СТАРТУ В НОВОМ ЧАТЕ

---

### 📌 АКТИВНАЯ ТЕМА И СТУПЕНЬ СБОРКИ:
* **Текущая тема:** {active_topic}
* **Входной Кубик на новый чат:** {entry_cube}
* **Командный мостик:** 👑 МАСТЕР_КАБИНА (Единый Штурвал)

---

### 🔑 ИНСТРУКЦИЯ ДЛЯ ИИ ПРИ СТАРТЕ В НОВОМ ЧАТЕ:
1. Прочитать данный `ПЕРЕХОДНЫЙ_МОСТ.md` за 1 секунду.
2. Подтвердить готовность 1 лаконичным предложением в левом чате.
3. Открыть на правом экране `РАБОЧИЙ_ДИАЛОГ.md` и продолжить работу с указанного Входного Кубика.

---

[📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md) | [🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)
"""

    with open(bridge_path_brain, "w", encoding="utf-8") as f:
        f.write(content)
        
    with open(bridge_path_caravan, "w", encoding="utf-8") as f:
        f.write(content)
        
    return {"bridge_brain": bridge_path_brain, "bridge_caravan": bridge_path_caravan}

if __name__ == "__main__":
    brain = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain/92f3f6f7-7f47-44fc-92e9-0ee82cb9e441"
    res = pack_bridge_for_new_chat(brain)
    print("=" * 60)
    print("🌉 УПАКОВКА ПЕРЕХОДНОГО МОСТА В НОВЫЙ ЧАТ (bridge_packer.py)")
    print("=" * 60)
    print(f"🔹 Мост упакован в сессию: {res['bridge_brain']}")
    print(f"🔹 Мост засинхронизирован в Караван: {res['bridge_caravan']}")
    print("=" * 60)
