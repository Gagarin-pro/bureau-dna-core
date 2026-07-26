---
name: n8n-manager
description: Skill to manage the remote n8n-dispatcher VM instance on GCP, check docker logs, restart containers, inspect database, and run diagnostics.
---

# 🧱 УМЕНИЕ: УПРАВЛЕНИЕ ОБЛАЧНЫМ n8n-ДИСПЕТЧЕРОМ (n8n-manager)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Данный модуль содержит физические адреса, регламенты сопряжения и консольные команды для администрирования и мониторинга ноды n8n-dispatcher на серверах Google Cloud Platform.

---

## 📡 ФИЗИЧЕСКИЙ АДРЕС И ТОЧКИ СВЯЗИ
*   **Имя VM-инстанса в GCP:** `n8n-dispatcher`
*   **Зона размещения:** `us-east1-b`
*   **Внешний IP-адрес:** `35.229.90.22`
*   **Схема доступа:** Через авторизованный сеанс Google Cloud Shell (отладчик Chrome, порт 9222) с помощью команды:
    ```bash
    gcloud compute ssh n8n-dispatcher --zone=us-east1-b
    ```

---

## 📁 СТРУКТУРА ПАПОК НА СЕРВЕРЕ
*   **Конфигурационный цех:** `/opt/n8n/` (содержит `docker-compose.yml` и папку `caddy/` с конфигурационным файлом `Caddyfile`).
*   **База данных n8n (SQLite):** `/var/lib/docker/volumes/n8n_n8n_data/_data/database.sqlite`
*   **Локальные SSL-сертификаты Caddy:** `/var/lib/docker/volumes/n8n_caddy_data/_data/`

---

## 🛠️ СПРАВОЧНИК КОНСОЛЬНЫХ КОМАНД

### 1. Проверка состояния контейнеров
Для диагностики статуса n8n и Caddy зайди в рабочий каталог и выполни:
```bash
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="cd /opt/n8n && docker compose ps"
```

### 2. Снятие системных логов (stdout + stderr)
Для сбора системных сообщений используй прямые обращения к логированию контейнеров:
```bash
# Логи диспетчера n8n
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="docker logs n8n 2>&1 | tail -n 50"

# Логи шлюза Caddy
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="docker logs caddy 2>&1 | tail -n 50"
```

### 3. Перезапуск или обновление служб
Если требуется перезапустить контейнеры после изменения конфигураций:
```bash
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="cd /opt/n8n && docker compose restart"
```
Для применения изменений в `docker-compose.yml` с пересборкой:
```bash
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="cd /opt/n8n && docker compose up -d --force-recreate"
```

### 4. Прямой аудит базы данных SQLite (через Python на хосте)
Для извлечения списка пользователей и проверки статуса активации выполни на сервере:
```bash
gcloud compute ssh n8n-dispatcher --zone=us-east1-b --command="sudo python3 -c \"
import sqlite3
conn = sqlite3.connect('/var/lib/docker/volumes/n8n_n8n_data/_data/database.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT email, firstName, lastName, settings FROM user')
print(cursor.fetchall())
conn.close()
\""
```

---

## ⚠️ РЕГЛАМЕНТЫ БЕЗОПАСНОСТИ И ОТК
1.  **Закон Напряжения в Розетке:** При любых проблемах с SSL-соединением (`TLSV1_ALERT_INTERNAL_ERROR`) проверяй наличие глобальной опции `default_sni 35.229.90.22` в `/opt/n8n/caddy/Caddyfile`. Без этой опции Caddy сбрасывает запросы клиентов, не отправляющих SNI.
2.  **Запас дискового пространства:** Периодически контролируй свободное место на диске VM (выполняй `df -h`). SQLite при частой записи логов может забить диск.
3.  **Сохранение сессии Cloud Shell:** Всегда проверяй, что отладчик Chrome активен, чтобы не запустить повторный ресурсоемкий цикл авторизации в gcloud.