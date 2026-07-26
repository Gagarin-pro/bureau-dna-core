---
name: gcloud-infrastructure-ops
description: "Системные команды администрирования хоста n8n-dispatcher в GCP: управление Docker-контейнерами, бэкапирование баз данных PostgreSQL, настройка прокси Caddy и SSL."
---

# 🛡️ УМЕНИЕ: АДМИНИСТРИРОВАНИЕ GCP И DOCKER (gcloud-infrastructure-ops)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Данное умение описывает стандарты обслуживания удаленного GCP-сервера `n8n-dispatcher` финансового конвейера «Монолит».

---

## 📡 1. УДАЛЕННЫЙ ДОСТУП И ИНСПЕКЦИЯ КОНТЕЙНЕРОВ

1.  **Точка подключения:** Подключение к хосту через SSH-шлюз `gcloud`:
    ```bash
    /Users/tur/google-cloud-sdk/bin/gcloud compute ssh n8n-dispatcher --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc
    ```
2.  **Проверка жизнедеятельности (ОТК-Статус):**
    Проверка активности всех узлов:
    ```bash
    docker ps -a
    ```
3.  **Логирование системных компонентов:**
    ```bash
    docker logs monolith-backend --tail 100
    docker logs monolith-bot --tail 100
    ```

---

## 💾 2. РЕЗЕРВНОЕ КОПИРОВАНИЕ И СОХРАННОСТЬ КАЗНЫ (POSTGRESQL)

1.  **Создание дампа базы данных:**
    Экспорт рабочего реестра пользователей и транзакций из Docker-контейнера СУБД:
    ```bash
    docker exec -t monolith-db pg_dumpall -c -U monolith_user > /tmp/monolith_db_backup.sql
    ```
2.  **Загрузка бэкапа локально на Mac:**
    Копирование дампа с удаленного хоста на MacBook Юрия:
    ```bash
    /Users/tur/google-cloud-sdk/bin/gcloud compute scp n8n-dispatcher:/tmp/monolith_db_backup.sql /Users/tur/Desktop/BACKUP_MONOLITH.sql --zone=us-east1-b --project=project-fd1f4ac2-39b3-41a5-bbc
    ```

---

## 🌐 3. НАСТРОЙКА CADDY-ШЛЮЗА И SSL СЕРТИФИКАТОВ

1.  **Редактирование конфигурации Caddyfile:**
    Маршрутизация внешних доменных запросов на внутренний Fastify API (порт 3000) и n8n (порт 5678):
    ```caddy
    35-229-90-22.sslip.io {
        reverse_proxy /api/* monolith-backend:3000
        reverse_proxy /n8n/* n8n:5678
    }
    ```
2.  **Перезапуск конфигурации Caddy:**
    Применение изменений без прерывания сессий пользователей:
    ```bash
    docker exec -w /etc/caddy caddy caddy reload
    ```