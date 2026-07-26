---
name: google-agents-orchestrator
description: Управление и оркестрация Google-агентов (Jules, AI Studio, Flow, Vids) через CDP, CLI и локальные сменные кабины Бюро.
---

# 🛸 УМЕНИЕ: ОРКЕСТРАЦИЯ GOOGLE-АГЕНТОВ (Google Agents Orchestrator)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Этот модуль содержит единый свод правил, команд и сценариев для управления и координации флота Google-агентов в рамках Универсального Автоматизатора.

---

## 🛠️ 1. GOOGLE JULES (Автономный облачный слесарь)
*   **Назначение:** Написание тяжелого кода, рефакторинг и авто-багфикс в облачной песочнице.
*   **Исполнительный контур:** Ветка `branch` (Закон Изоляции).
*   **Команды управления:**
    *   `npx @google/jules login` — авторизация по именному пропуску КВС.
    *   `npx @google/jules new --repo <owner/repo> "Инструкция ТЗ"` — отправка задачи на облачный станок.
    *   `npx @google/jules remote pull --session <ID> --apply` — забрать готовую деталь (код) на Mac.
*   **ОТК-проверка:** Запуск ревизора `otk_auditor.py` и синтаксическая валидация (`node --check` / `python3 -m py_compile`).

---

## 🔑 2. GOOGLE AI STUDIO (Широкое Конструкторское Бюро)
*   **Назначение:** Глубокие архитектурные расчеты без когнитивной амнезии (контекст до 2 млн токенов).
*   **Сценарий загрузки Snapshots:**
    1.  Запуск архивиста для сборки кодовой базы в один файл:
        `python3 "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts/git_archivist.py"`
    2.  Импорт полученного `.txt` файла в левую панель [aistudio.google.com](https://aistudio.google.com/).
*   **Регулировка моторов:**
    *   `Gemini 1.5 Pro` (Temp: 0.0) — для сборки кода и строгого анализа.
    *   `Gemini 1.5 Flash` (Temp: 1.0) — для быстрого мозгового штурма и сжатия прицепов памяти.

---

## 🎬 3. GOOGLE FLOW & GOOGLE VIDS (Визуализаторы и Veo 3.1)
*   **Назначение:** Генерация кинематографических видеороликов и раскадровка видеопрезентаций Бюро.
*   **Связующий мост (Chrome CDP):**
    *   Запуск Chrome в режиме отладки:
        `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/Users/tur/Desktop/notebook_lm_school/chrome_profile" &`
    *   **Ввод текста (React-формы):** Применение Range/Selection API во избежание потери фокуса:
        `document.execCommand('insertText', false, 'Промпт для Veo...');`
    *   **Удержание активности:** Холостой пинг вкладки `Runtime.evaluate` каждые 30 секунд для предотвращения засыпания вкладок на macOS.
    *   **Экспорт результатов:** Перенос скачанных роликов в каталог `/05_ИССЛЕДОВАНИЯ/видео/` с записью метаданных в журнал смены.

---

## 📡 4. УПРАВЛЕНИЕ ФОКУСОМ ЭКРАНА (Target Focus)
Для вызова нужного агента на передний план экрана Юрия используется CDP-метод `Target.activateTarget`:
```python
async def focus_agent_tab(ws, target_url_part):
    # Опрос вкладок
    tabs = await get_all_tabs(ws)
    for tab in tabs:
        if target_url_part in tab["url"]:
            # Активировать вкладку на экране
            await ws.send(json.dumps({
                "method": "Target.activateTarget",
                "params": {"targetId": tab["targetId"]}
            }))
```