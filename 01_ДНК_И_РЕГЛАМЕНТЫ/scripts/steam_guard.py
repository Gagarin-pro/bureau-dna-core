import os, sys, json, shutil

MASTER_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

def assemble_transition_bridge(brain_folder, tokens):
    bridge_content = f"""# 🌉 КАТАПУЛЬТА В НОВЫЙ ДИАЛОГ (ПЕРЕХОДНЫЙ МОСТ)
> **Режим:** АВТОМАТИЧЕСКАЯ СБОРКА СТОРОЖЕМ (`steam_guard.py`) | **Давление котлов:** ~{tokens:,} токенов (100% ПОРОГ ПЕРЕХОДА)
> **Дата сборки:** 24 июля 2026 | **Статус:** 🟢 ГОТОВ К МГНОВЕННОЙ ИНИЦИАЛИЗАЦИИ

---

### 📜 1. СВОДКА ПРЕПЯТСТВИЙ И ВСЕХ ПОБЕД СМЕНЫ:
* **Победа #147:** Калькулятор и Мост связи под ключ.
* **Победа #148:** Навигатор Моделей и `cognitive-fuel-advisor`.
* **Победа #149:** Математический аудит списания квот (1% часового = ~726.6 токенов).
* **Победа #150:** Супер-умение `atomic-batch-executor` (50% экономии топлива).
* **Победа #151:** Сравнительный аудит чатов (выгрузка отчетов сберегает 25.9% токенов).
* **Победа #152:** Аудит видеоурока Ромы Райта ($2M) и создание 63-го умения `product-growth-architect`.
* **Победа #153:** Сплошной аудит 63 умений по 5 операционным кластерам.
* **Победа #154:** Модернизация 63 умений Бюро скриптом `skills_optimizer.py`.
* **Победа #155:** Монитор пара `steam_pressure_monitor.py` и калибровка реального веса.
* **Победа #156:** Фоновый Сторож Давления `steam_guard.py` и Авто-Сборка Моста под ключ!

---

### 🛡️ 2. ДЕЙСТВУЮЩИЙ КАРАВАН И СТАНДАРТЫ БЮРО:
1. **Закон Атомарного Пакетного Вызова (`atomic-batch-executor`)**: Чтение и правка файлов за 1 параллельный шаг.
2. **Закон Сверх-Сжатого Левого Вакуума**: Выгрузка отчетов строго в `РАБОЧИЙ_ДИАЛОГ.md` (15 токенов в UI).
3. **Закон Автоматического Сторожа Пара**: Контроль Порога 1 000 000 токенов под ключ.

---

### 🚀 3. ИНСТРУКЦИЯ КВС ЮРИЮ ДЛЯ ПЕРЕХОДА ЗА 1 СЕКУНДУ:
1. Нажми **«+ New Conversation»** в верхнем левом углу Antigravity.
2. Отправь короткую команду:
   ```text
   BUREAU_SETUP продолжаем
   ```
3. ИИ-Архитектор моментально подхватит этот `ПЕРЕХОДНЫЙ_МОСТ.md`, проведет префлайт и за 1 секунду возобновит смену без потери контекста!

---

[🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md)
"""
    # Write to local brain artifact folder
    local_bridge = os.path.join(brain_folder, "ПЕРЕХОДНЫЙ_МОСТ.md")
    with open(local_bridge, "w", encoding="utf-8") as f:
        f.write(bridge_content)
        
    local_meta = {
        "UserFacing": True,
        "RequestFeedback": True,
        "Summary": "Когнитивный переходный мост, автоматически собранный Сторожем steam_guard.py."
    }
    with open(local_bridge + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(local_meta, f, indent=2, ensure_ascii=False)
        
    # Write to Google Drive Caravan
    drive_bridge = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПЕРЕХОДНЫЙ_МОСТ.md")
    with open(drive_bridge, "w", encoding="utf-8") as f:
        f.write(bridge_content)
        
    return True

def inject_warning_banner(brain_folder, res):
    rd_path = os.path.join(brain_folder, "РАБОЧИЙ_ДИАЛОГ.md")
    if not os.path.exists(rd_path):
        return
    with open(rd_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    banner_marker = "<!-- STEAM_GUARD_BANNER_START -->"
    if banner_marker in content:
        parts = content.split("<!-- STEAM_GUARD_BANNER_END -->")
        if len(parts) > 1:
            content = parts[1].lstrip()
        else:
            content = content.split(banner_marker)[0]

    banner = ""
    if res["status"] == "AUTO_TRANSITION_ASSEMBLED":
        banner = f"""<!-- STEAM_GUARD_BANNER_START -->
> [!CAUTION]
> 🚨 **КРАСНЫЙ УРОВЕНЬ ДАВЛЕНИЯ ПАРА ({res['tokens']:,} токенов / >1M):** 
> Котлы переполнены! Сторож `steam_guard.py` **АВТОМАТИЧЕСКИ ЗАПЕЧАТАЛ ПЕРЕХОДНЫЙ МОСТ**! 
> Пора переехать в чистый чат: откройте `Cmd + N` и отправьте `поехали`.

<!-- STEAM_GUARD_BANNER_END -->

"""
    elif res["status"] in ("WARNING_ORANGE", "WARNING_YELLOW"):
        banner = f"""<!-- STEAM_GUARD_BANNER_START -->
> [!WARNING]
> ⚠️ **ЖЕЛТЫЙ ПРЕДУПРЕДИТЕЛЬНЫЙ УРОВЕНЬ ПАРА ({res['tokens']:,} токенов / >800K):** 
> Давление пара высокое. Сторож `steam_guard.py` подготавливает сменные прицепы памяти.

<!-- STEAM_GUARD_BANNER_END -->

"""
    if banner:
        with open(rd_path, "w", encoding="utf-8") as f:
            f.write(banner + content)

def run_steam_guard(brain_folder):
    log_file = os.path.join(brain_folder, ".system_generated/logs/transcript_full.jsonl")
    if not os.path.exists(log_file):
        log_file = os.path.join(brain_folder, ".system_generated/logs/transcript.jsonl")
        
    if not os.path.exists(log_file):
        return {"status": "NORMAL", "tokens": 0, "msg": "Лог файл не найден."}
        
    log_bytes = os.path.getsize(log_file)
    tokens = log_bytes // 4
    
    if tokens >= 1000000:
        assemble_transition_bridge(brain_folder, tokens)
        res = {
            "status": "AUTO_TRANSITION_ASSEMBLED",
            "tokens": tokens,
            "msg": f"🔴 КРАСНЫЙ ПОРОГ (1M токенов): Сторож steam_guard.py АВТОМАТИЧЕСКИ СОБРАЛ ПЕРЕХОДНЫЙ_МОСТ.md!"
        }
    elif tokens >= 800000:
        res = {
            "status": "WARNING_YELLOW",
            "tokens": tokens,
            "msg": f"⚠️ ПРЕДУПРЕЖДЕНИЕ (800K токенов): Давление котлов достигло {tokens:,} токенов."
        }
    else:
        res = {
            "status": "GREEN_NORMAL",
            "tokens": tokens,
            "msg": f"🟢 ЛЕДЯНОЙ РЕЖИМ ({tokens:,} токенов): Сторож ведет непрерывный молчаливый контроль."
        }
    
    inject_warning_banner(brain_folder, res)
    return res

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    res = run_steam_guard(b_folder)
    print("=" * 60)
    print("🛡️ ФОНОВЫЙ СТОРОЖ ДАВЛЕНИЯ ПАРА И АВТО-МОСТ (steam_guard.py)")
    print("=" * 60)
    print(f"🔹 Статус Сторожа: {res['status']}")
    print(f"🔹 Физическое значение пара: ~{res['tokens']:,} токенов")
    print(f"🔹 Системное сообщение: {res['msg']}")
    print("=" * 60)
