---
name: telemetry-analytics
description: Анализ пользовательских логов телеметрии, переписки чата и плотности переходов на базе PostgreSQL.
---

# 📊 НАВЫК ТЕЛЕМЕТРИИ, АНАЛИЗА ЛОГОВ И ЧАТ-АНАЛИТИКИ

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Этот навык описывает методы сбора, структурирования и анализа действий пользователей и логов переписки в приложении TWA на базе PostgreSQL.

## 🛠️ СТРУКТУРА ДАННЫХ И ТАБЛИЦЫ БД

### 1. События интерфейса (`telemetry_logs`)
Все события TWA пишутся в таблицу `telemetry_logs`:
- `telegram_id` (bigint): Идентификатор пользователя.
- `action_name` (varchar): Название действия (например, 'app_loaded', 'switch_tab', 'click_button').
- `metadata` (jsonb): Дополнительные параметры действия (например, `{ "tab": "admin" }`).
- `created_at` (timestamp): Время совершения действия.

### 2. Чат-Стенограмма (`chat_scout_logs`)
Сообщения команды разработчиков и импортируемые диалоги пишутся в таблицу `chat_scout_logs`:
- `id` (serial primary key): Идентификатор записи.
- `msg_time` (timestamp): Время получения сообщения.
- `chat_title` (varchar): Название чата или признак источника (например, 'Личные сообщения').
- `username` (varchar): Имя отправителя + отметка о пересылке (например, `Gagaryn_pro [Переслано от star_rom]`).
- `message_text` (text): Содержание сообщения или описание медиафайла.

---

## 📡 АРХИТЕКТУРА СЕРВЕРНЫХ ВЕБХУКОВ (WEBHOOKS)

Для надежной интеграции с мессенджерами используется Fastify-приемник:
1. **Точка входа:** `POST /api/chat-scout` (защищена SSL Caddy-прокси).
2. **Фильтрация отправителей:** При получении сообщений в личных чатах (type: private) бот проверяет имя отправителя по белому списку доверенных аккаунтов (например, `Gagaryn_pro`).
3. **Распознавание пересланных сообщений (Forward parser):**
   * При наличии `msg.forward_from` оригинальный автор определяется по `username` или `first_name`.
   * При наличии `msg.forward_sender_name` (если пользователь скрыл профиль) имя автора берется оттуда.
4. **Конвертация медиа-контента:**
   * Голосовые: `🎙️ [Голосовое сообщение, {duration} сек]`
   * Файлы: `📄 [Файл: {file_name}]`
   * Стикеры: `👾 [Стикер {emoji}]`

---

## 📈 КЛЮЧЕВЫЕ МЕТОДЫ АНАЛИЗА (SQL-ЗАПРОСЫ)

### 1. Расчет общей конверсии переходов по табам:
```sql
SELECT 
    action_name,
    metadata->>'tab' AS tab_name,
    COUNT(*) AS total_clicks,
    COUNT(DISTINCT telegram_id) AS unique_users
FROM telemetry_logs
WHERE action_name = 'switch_tab'
GROUP BY action_name, tab_name
ORDER BY total_clicks DESC;
```

### 2. Построение воронки активации уровней:
```sql
SELECT 
    step,
    COUNT(DISTINCT telegram_id) AS user_count
FROM (
    SELECT telegram_id, '1_app_loaded' AS step FROM telemetry_logs WHERE action_name = 'app_loaded'
    UNION ALL
    SELECT telegram_id, '2_click_activation' AS step FROM telemetry_logs WHERE action_name = 'select_level_activation'
    UNION ALL
    SELECT telegram_id, '3_confirm_purchase' AS step FROM telemetry_logs WHERE action_name = 'buy_level_from_balance'
) sub
GROUP BY step
ORDER BY step;
```

### 3. Выгрузка переписки чата:
```sql
SELECT msg_time, chat_title, username, message_text 
FROM chat_scout_logs 
ORDER BY id DESC 
LIMIT 10;
```
