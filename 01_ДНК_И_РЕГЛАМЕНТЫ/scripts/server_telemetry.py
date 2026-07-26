#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUCTOR-ARCHITECT PRO — Агент «Сенсор Телеметрии Сервера»
Назначение: Сбор статуса Docker-контейнеров, метрик БД Postgres и системных ресурсов в единый отчет.
"""

import subprocess
import json
import os

def get_docker_status():
    containers = ["monolith-backend", "monolith-bot", "monolith-db", "n8n", "caddy"]
    status_dict = {}
    for c in containers:
        try:
            cmd = f"sudo docker inspect --format='{{{{.State.Status}}}}' {c}"
            status = subprocess.check_output(cmd, shell=True, text=True).strip()
            status_dict[c] = status
        except Exception:
            status_dict[c] = "offline"
    return status_dict

def query_db(sql):
    try:
        cmd = f"sudo docker exec monolith-db psql -U monolith_user -d monolith_db -t -c \"{sql}\""
        out = subprocess.check_output(cmd, shell=True, text=True).strip()
        return out
    except Exception:
        return None

def get_db_metrics():
    metrics = {
        "status": "offline",
        "users_count": 0,
        "payments_count": 0,
        "last_payments": []
    }
    try:
        # Check if container is running
        cmd = "sudo docker inspect --format='{{.State.Status}}' monolith-db"
        status = subprocess.check_output(cmd, shell=True, text=True).strip()
        if status != "running":
            metrics["status"] = f"container status: {status}"
            return metrics
        
        # 1. Считаем пользователей
        users_out = query_db("SELECT COUNT(*) FROM users;")
        if users_out:
            metrics["users_count"] = int(users_out.strip())
            
        # 2. Считаем платежи
        payments_out = query_db("SELECT COUNT(*) FROM payments;")
        if payments_out:
            metrics["payments_count"] = int(payments_out.strip())
            
        # 3. Берем последние 3 платежа
        sql_last = "SELECT p.id, u.username, p.amount, p.status, p.created_at FROM payments p JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC LIMIT 3;"
        cmd_last = f"sudo docker exec monolith-db psql -U monolith_user -d monolith_db -t -A -F ',' -c \"{sql_last}\""
        rows_out = subprocess.check_output(cmd_last, shell=True, text=True).strip().split('\n')
        
        for row in rows_out:
            if not row.strip():
                continue
            parts = row.split(',')
            if len(parts) >= 5:
                metrics["last_payments"].append({
                    "id": int(parts[0]),
                    "username": parts[1],
                    "amount": float(parts[2]),
                    "status": parts[3],
                    "created_at": parts[4]
                })
        metrics["status"] = "online"
    except Exception as e:
        metrics["status"] = f"error: {str(e)}"
    return metrics

def get_sys_resources():
    resources = {
        "disk_free": "0GB",
        "memory_free": "0MB"
    }
    try:
        # Disk usage
        df = subprocess.check_output("df -h / | tail -1 | awk '{print $4}'", shell=True, text=True).strip()
        resources["disk_free"] = df
        
        # Memory usage
        mem = subprocess.check_output("free -m | grep Mem | awk '{print $4}'", shell=True, text=True).strip()
        resources["memory_free"] = f"{mem}MB"
    except Exception:
        pass
    return resources

def get_chat_scout_logs():
    sql = "SELECT msg_time, chat_title, username, message_text FROM chat_scout_logs ORDER BY id DESC LIMIT 10;"
    cmd = f"sudo docker exec monolith-db psql -U monolith_user -d monolith_db -t -A -F ',' -c \"{sql}\""
    try:
        out = subprocess.check_output(cmd, shell=True, text=True).strip()
        if not out:
            return []
        rows = out.split('\n')
        logs = []
        for r in rows:
            if r.strip():
                # Упрощенное разбиение по запятой
                parts = r.split(',')
                if len(parts) >= 4:
                    logs.append(f"[{parts[0]}] [{parts[1]}] {parts[2]}: {parts[3]}")
        return logs
    except Exception as e:
        return [f"Ошибка чтения БД чата: {str(e)}"]

def generate_report():
    report = {
        "docker": get_docker_status(),
        "database": get_db_metrics(),
        "system": get_sys_resources(),
        "chat_scout": get_chat_scout_logs()
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    generate_report()

