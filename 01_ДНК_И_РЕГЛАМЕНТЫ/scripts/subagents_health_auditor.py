#!/usr/bin/env python3
import os, sys, py_compile

SCRIPTS_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts")

AGENTS = [
    {"name": "skills_scout.py", "role": "Фоновый Скаут Новых Умений & Ревизор ДНК"},
    {"name": "steam_guard.py", "role": "Фоновый Сторож Давления Пара & Переходный Мост"},
    {"name": "cabins_hermetic_guard.py", "role": "Замок Герметичности 7 Кабин Бюро"},
    {"name": "cabin_memory_recall.py", "role": "Двигатель Дневного Архивирования ДИАЛОГИ/"},
    {"name": "agenda_auto_sync.py", "role": "Авто-Синхронизатор 4-й Кнопки ПЛАНЕРКИ/"},
    {"name": "footer_guard_enforcer.py", "role": "Страж 5-Кнопочной Панели Electron"},
]

def audit_subagents_health():
    statuses = []
    all_healthy = True

    for agent in AGENTS:
        path = os.path.join(SCRIPTS_DIR, agent["name"])
        if not os.path.exists(path):
            statuses.append({"name": agent["name"], "role": agent["role"], "status": "🔴 MISSING", "healthy": False})
            all_healthy = False
            continue

        try:
            py_compile.compile(path, doraise=True)
            statuses.append({"name": agent["name"], "role": agent["role"], "status": "🟢 HEALTHY (Syntax OK)", "healthy": True})
        except Exception as e:
            statuses.append({"name": agent["name"], "role": agent["role"], "status": f"🔴 ERROR ({e})", "healthy": False})
            all_healthy = False

    return {"all_healthy": all_healthy, "agents": statuses}

if __name__ == "__main__":
    res = audit_subagents_health()
    print("=" * 65)
    print("🤖 АВТО-ДИАГНОСТИКА ЗДОРОВЬЯ СУБАГЕНТОВ (subagents_health_auditor.py)")
    print("=" * 65)
    for a in res["agents"]:
        print(f"🔹 [{a['status']}] {a['name']} — {a['role']}")
    print("=" * 65)
    print(f"🔹 Итоговый статус экипажа: {'🟢 100% ЗДОРОВЫ И В СТРОЮ' if res['all_healthy'] else '🔴 ОБНАРУЖЕНЫ СБОИ'}")
    print("=" * 65)
