import os, sys, re

MASTER_TEMPLATE = "/Users/tur/.gemini/config/autonomous_bureau_dashboard_master.md"
MASTER_DIR = "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"

CLEAN_MASTER_CONTENT = """# 🧱 АВТОНОМНОЕ БЮРО ПРОЕКТИРОВАНИЯ — ПАНЕЛЬ УПРАВЛЕНИЯ
> **Версия панели:** 3.1 (Очищенный Мастер-Релиз) | **Дата:** 24 июля 2026 | **Генеральный Конструктор:** Юрий

Эта панель выведена на ваш правый экран для контроля сборочных кабин и флота автономных агентов.

---

## 🚨 КОНТУР СОВМЕСТНОЙ АКТИВНОСТИ (КВС ⇄ АВТОМАТИЗАТОР)

*   **Активный сборочный верстак:** 🟢 МАСТЕР_КАБИНА [Главный штаб Бюро & Центр Antigravity]
*   **Ресурс внимания КВС (Фокус):** 🟢 ВЫСОКИЙ (Двойное рукопожатие на фокус активно)

---

## 🤖 РАСПИСАНИЕ ФЛОТА АВТОНОМНЫХ АГЕНТОВ (AGENT FLEET STATUS)

Наш флот ИИ-агентов готов выполнять любые прикладные поручения КВС:

| Имя / Идентификатор | Роль агента на заводе | Статус работы | Текущая задача / Направление |
| :--- | :--- | :---: | :--- |
| **Antigravity** | Главный Личный Автоматизатор | 🟢 Активен | Управление планеркой и сменными приборами |
| **Когнитивный Аудитор** | Исследователь истории смен | 🟢 Готов | Ревизор диалогов и физических логов Mac |
| **Внешний Скаут Умений (`skills_scout.py`)** | 🟢 Авто-Запуск | Фоновая разведка GitHub API на предмет новых ИИ-умений | 🟢 Запускается автоматически при старте смены |
| **ИИ-Писец смены (`shift_agent.py`)** | Локальный архивариус смены | ⏳ Ожидание | Ждет завершения смены для записи рапорта |
| **Слесарь-Кодер (Jules)** | Облачный сборщик тяжелого кода | ⏳ Ожидание | Готов к развертыванию облачных Fastify-серверов |
| **Давление в котлах (Длина чата)** | 🟢 Ледяной режим | Замер накопленного пара (объема текста диалога и файлов) | {{TOKEN_COUNT}} |
| **Топливный бак (Квоты Моделей)** | 🟢 Очищено (#160) | Оптимизация Пульта Управления | 7 Профессиональных Кабин & 5 Эталонных Кнопок под ключ |
| **Мост Гагарин (Mac ⇄ Облако)** | 🟢 Активен | Фоновый мост связи файлов Mac с облачным сервером | 🟢 Активен (Go (Соединение стабильно)) |
| **Диспетчер автоматики (n8n)** | 🟢 Активен | Облачный диспетчерский пункт на сервере GCP | 🟢 Активен (Go (Шлюз SSL Caddy активен)) |
| **Ревизор Картотеки** | 🟢 Активна (Файлы Mac) | Датчик инвентаризации когнитивных умений | 🟢 63 уникальных умений активны |

---

## 📂 КАРТОТЕКА АКТИВНЫХ КАБИН (7 СБОРОЧНЫХ ВЕРСТАКОВ БЮРО)

Вы можете переключить Бюро в любой из 7 профессиональных цехов одной командой:

* 👑 **`МАСТЕР_КАБИНА`** [Активна по умолчанию] — **Главный штаб Бюро & Центр Antigravity**: Управление сменами, координация кабин, отладка MCP-серверов и прошивка ДНК. ([`СТАТУС_ПРОЕКТА.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/СТАТУС_ПРОЕКТА.md))
* 📜 **`BUKVITSA_BOT`** — **Цех Славяно-Арийской Нумерологии и Буквицы**: Матрица 49 Кодов, AlMAM Digital Ark, расчет Кона (52/7) и Буквиц. ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Буквица-бот/NAVIGATOR.md))
* 🏭 **`MONOLITH`** — **Финансово-Маркетинговый Цех «Монолит»**: Telegram Mini App (TWA Canvas), Telegram-бот, Fastify REST API, СУБД PostgreSQL. ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/06_ЦЕХ_МОНОЛИТ/NAVIGATOR.md))
* ⚖️ **`COURT_CASE`** — **Правовой Цех (ИИ-Юрист Юрия)**: Судебная защита, медицинские ходатайства, ГАС «Правосудие», ГОСТ-печать (`print_assistant.py`). ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/08_ЛИЧНЫЙ_КАРАВАН/NAVIGATOR.md))
* 🚀 **`AUTOSCHOOL`** — **Учебный Цех «Автошкола ИИ» и ОС Гагарин**: Обучающие материалы NotebookLM, диспетчеризация n8n на GCP, ИИ-Агент Гагарин. ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/02_ЦЕХ_ГАГАРИН/NAVIGATOR.md))
* 🧪 **`AI_STUDIO_RD`** — **Научно-Исследовательский Цех Google AI Studio**: Модель Gemini 2M, Ресурсная экономика Жака Фреско, R&D Бюро. ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Google%20AI%20Studio%20—%20База%20R&D/NAVIGATOR.md))
* 🛡️ **`VPN_REALITY`** — **Цех Безопасности и Туннелей VPN Reality**: VLESS Reality туннели, генерация ключей доступа и управление пользователями Xray. ([`NAVIGATOR.md`](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/NAVIGATOR.md))

---

## 🗺️ КАРТА НАКОПЛЕННОГО ДОСТОЯНИЯ И АКТИВОВ БЮРО

Инвентаризация совместного опыта, 7 сборочных отделов, 159 побед и каналов связи:

| Отдел / Категория | Содержание и состав активов | Локация и Ссылка на чертежи |
| :--- | :--- | :--- |
| 📜 **01_ДНК_И_РЕГЛАМЕНТЫ** | Устав PRO-3.0, 63 модернизированных умений, 8 скриптов авто-диагностики (`start_shift.py`, `cabins_consolidator.py` и др.) | [01_ДНК_И_РЕГЛАМЕНТЫ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ) |
| 🚀 **02_ЦЕХ_ГАГАРИН & VPN** | Сборочные чертежи ИИ-Агента Гагарин (`Gagarin_OS.app`) и VPN Центр (`ssh_manager.py`, VLESS Reality) | [02_ЦЕХ_ГАГАРИН](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/02_ЦЕХ_ГАГАРИН) |
| 📕 **03_БОРТОВОЙ_КАРАВАН** | Компас Сборки (Якорь 136), `ПРИЦЕП_ПАМЯТИ.md`, `ПОВЕСТКА_ПЛАНЕРКИ.md`, `ЖУРНАЛ_ЛАБОРАТОРНЫХ_ИСПЫТАНИЙ.md` (159 Побед) | [03_БОРТОВОЙ_КАРАВАН](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН) |
| 📱 **06_ЦЕХ_МОНОЛИТ** | Telegram Mini App (TWA Canvas), Telegram-бот, Fastify REST API, СУБД PostgreSQL | [06_ЦЕХ_МОНОЛИТ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/06_ЦЕХ_МОНОЛИТ) |
| ⚖️ **08_ЛИЧНЫЙ_КАРАВАН** | ИИ-Юрист `COURT_CASE`: Судебная защита, медицинские ходатайства, ГАС «Правосудие», ГОСТ-печать `print_assistant.py` | [08_ЛИЧНЫЙ_КАРАВАН](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/08_ЛИЧНЫЙ_КАРАВАН) |
| 🛠️ **Когнитивный Стек** | 63 Активных умений ИИ (`truth-auditor`, `atomic-batch-executor`, `agent-orchestrator`) в меню `Customizations` | [Картотека умений](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md) |
| 🔌 **Исполнительные Мосты** | Мост Гагарина (`gagarin_bridge_v2`), облачный Диспетчер n8n GCP, шина GUI Electron (Side-by-side) | [Дистрибутив Моста](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/04_ДИСТРИБУТИВ/gagarin_bridge_v2) |

---

## 🕹️ ПУЛЬТ ЭКСПРЕСС-КОМАНД ВАЙБ-КОДИНГА (ГОРЯЧИЕ РЫЧАГИ)

Введите команду в левый чат для управления фабрикой:

| Команда-Рычаг | Описание действия | Физический результат |
| :--- | :--- | :--- |
| `BUREAU_SETUP продолжаем` | Начать / продолжать работу | Авто-диагностика смены, загрузка навигатора, сверка логов |
| `BUREAU_SETUP переключить на <ИМЯ_КАБИНЫ>` | Переключить активный верстак | Мгновенный перенос фокуса ИИ в выбранный цех |
| `BUREAU_SETUP завершить` | Закрыть рабочую смену | Рапорт ИИ-Писца, архивация памяти, очистка котлов |

---

[🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)
"""

def optimize_dashboard():
    with open(MASTER_TEMPLATE, "w", encoding="utf-8") as f:
        f.write(CLEAN_MASTER_CONTENT)
    return True

if __name__ == "__main__":
    if optimize_dashboard():
        print("=" * 60)
        print("📟 ГЛУБОКАЯ ОПТИМИЗАЦИЯ ПУЛЬТА УПРАВЛЕНИЯ (dashboard_optimizer.py)")
        print("=" * 60)
        print("🔹 Дубликаты кабин в Контуре Активности вычищены (оставлена только МАСТЕР_КАБИНА)")
        print("🔹 Битая ссылка на картотеку умений исправлена на живой путь 63 умений")
        print("🔹 Картотека кабин сокращена до 7 Чистых Профессиональных Кабин Бюро")
        print("🔹 Внедрен Эталонный 5-Кнопочный Навигатор в подвал мастера-шаблона")
        print("=" * 60)
        print("🟢 МАСТЕР-ШАБЛОН autonomous_bureau_dashboard_master.md УСПЕШНО ОБНОВЛЕН!")
        print("=" * 60)
