---
name: monolith-manager
description: Модуль управления финансовым конвейером «Монолит» в Docker-окружении на удаленном сервере GCP VM. Содержит команды мониторинга логов, перезапуска контейнеров и проверки базы данных.
---

# 🧱 УМЕНИЕ: УПРАВЛЕНИЕ ХОСТОМ «МОНОЛИТА» (monolith-manager)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Данный модуль содержит физические адреса подстанций, команды управления и регламенты технического надзора за финансовым конвейером «Монолит» на серверах Google Cloud Platform.

---

## 📡 ФИЗИЧЕСКИЙ АДРЕС И ТОЧКИ СВЯЗИ
*   **Имя VM-инстанса в GCP:** `n8n-dispatcher` (наш объединенный хост)
*   **Зона размещения:** `us-east1-b`
*   **GCP Проект:** `project-fd1f4ac2-39b3-41a5-bbc`
*   **Внешний IP-адрес:** `35.229.90.22`
*   **Схема доступа:** Через утилиту `gcloud` на локальном MacBook с явным указанием пути:
    ```bash
    /Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc
    ```

---

## 🐋 СПРАВОЧНИК КОНСОЛЬНЫХ КОМАНД СБОРКИ И НАДЗОРА

### 1. Проверка состояния кают (контейнеров)
Чтобы увидеть статус работы бэкенда, бота и базы данных, выполни:
```bash
/Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc --command="docker ps -a"
```

### 2. Снятие системных логов
Для чтения последних записей о жизнедеятельности Fastify-двигателя или Telegram-бота:
```bash
# Логи бэкенда (Fastify API)
/Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc --command="docker logs monolith-backend --tail 50"

# Логи Telegram-бота
/Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc --command="docker logs monolith-bot --tail 50"
```

### 3. Перезапуск узлов
При зависании или обновлении кодовых файлов:
```bash
# Перезапуск бэкенда и бота
/Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc --command="docker restart monolith-backend monolith-bot"
```

### 4. Опрос картотеки PostgreSQL из терминала Mac (через Docker exec на сервере)
Чтобы выполнить SQL-запрос напрямую в СУБД на удаленном сервере:
```bash
/Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc --command="docker exec -i monolith-db psql -U monolith_user -d monolith_db -c 'SELECT COUNT(*) FROM users;'"
```

---

## 🛡️ ОТК-РЕГЛАМЕНТЫ БЕЗОПАСНОСТИ
1.  **Чистота контуров:** Запрещено разворачивать базы данных или бэкенд проекта «Монолит» на Сервере №1 (`216.57.106.146`), который выделен строго под VPN-мосты.
2.  **Защита live-данных:** При проведении симуляций или тестирования функционала, тест-кейсы должны быть изолированы (локальная симуляция на Mac или временная схема базы данных на сервере №2), чтобы исключить повреждение рабочих профилей пользователей.