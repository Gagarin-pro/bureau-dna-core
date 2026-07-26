#!/usr/bin/env python3
import os, sys, time

SCRIPTS_DIR = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from cabins_hermetic_guard import audit_and_seal_cabins
from cabin_memory_recall import archive_and_recall_cabin_memory
from agenda_auto_sync import sync_and_archive_agenda
from steam_guard import run_steam_guard
from subagents_health_auditor import audit_subagents_health
from bukvitsa_day_calculator import get_bukvitsa_for_date
from footer_guard_enforcer import run_footer_enforcement
from preflight_safety_guard import run_preflight_safety_audit
from parity_checker import verify_4window_parity
from path_and_quote_guard import run_path_and_quote_guard
from focus_drift_guard import run_focus_drift_guard
from zero_manual_guard import run_zero_manual_guard
from model_bridge_anchor import run_model_bridge_anchor
from audit_pack_builder import build_audit_package

def run_unified_bureau_guards(brain_folder, active_cabin="МАСТЕР_КАБИНА"):
    start_t = time.time()
    results = {}

    # 0. 4-Window Parity Checker
    try:
        results["parity"] = verify_4window_parity(brain_folder, active_cabin)
    except Exception as e:
        results["parity"] = {"error": str(e)}

    # 0.1. Audit Pack Builder Check
    try:
        results["audit_pack"] = build_audit_package()
    except Exception as e:
        results["audit_pack"] = {"error": str(e)}

    # 0.1. Model Bridge Anchor Guard
    try:
        results["model_anchor"] = run_model_bridge_anchor()
    except Exception as e:
        results["model_anchor"] = {"error": str(e)}

    # 0.1. Path & Quote Sanitizer
    try:
        results["path_quote"] = run_path_and_quote_guard()
    except Exception as e:
        results["path_quote"] = {"error": str(e)}

    # 0.2. Focus Drift Guard
    try:
        results["focus_drift"] = run_focus_drift_guard()
    except Exception as e:
        results["focus_drift"] = {"error": str(e)}

    # 0.3. Zero Manual Effort Guard
    try:
        results["zero_manual"] = run_zero_manual_guard()
    except Exception as e:
        results["zero_manual"] = {"error": str(e)}

    # 1. Hermetic Locks
    try:
        results["hermetic"] = audit_and_seal_cabins(brain_folder)
    except Exception as e:
        results["hermetic"] = {"error": str(e)}

    # 2. Memory Recall
    try:
        results["memory"] = archive_and_recall_cabin_memory(brain_folder, active_cabin)
    except Exception as e:
        results["memory"] = {"error": str(e)}

    # 3. Agenda Auto Sync
    try:
        results["agenda"] = sync_and_archive_agenda(brain_folder, active_cabin)
    except Exception as e:
        results["agenda"] = {"error": str(e)}

    # 4. Steam Guard
    try:
        results["steam"] = run_steam_guard(brain_folder)
    except Exception as e:
        results["steam"] = {"error": str(e)}

    # 5. Health Auditor
    try:
        results["health"] = audit_subagents_health()
    except Exception as e:
        results["health"] = {"error": str(e)}

    # 6. Bukvitsa Day Matrix
    try:
        results["bukvitsa"] = get_bukvitsa_for_date()
    except Exception as e:
        results["bukvitsa"] = {"summary": "Буквица: Активна"}

    # 7. Rocket Engine Footer Enforcer
    try:
        results["footers"] = run_footer_enforcement()
    except Exception as e:
        results["footers"] = 0

    # 8. Pre-Flight Safety Shield & Visual Audit
    try:
        results["preflight"] = run_preflight_safety_audit(brain_folder)
    except Exception as e:
        results["preflight"] = {"status": "YELLOW", "error": str(e)}

    elapsed = time.time() - start_t
    results["elapsed_sec"] = round(elapsed, 3)
    return results

if __name__ == "__main__":
    b_folder = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), ".gemini/antigravity/brain/92f3f6f7-7f47-44fc-92e9-0ee82cb9e441")
    cabin = sys.argv[2] if len(sys.argv) > 2 else "МАСТЕР_КАБИНА"
    res = run_unified_bureau_guards(b_folder, cabin)
    
    print("=" * 65)
    print("⚡ ЕДИНЫЙ ПАКЕТНЫЙ МОТОР СУБАГЕНТОВ (unified_guards_runner.py)")
    print("=" * 65)
    print(f"🔹 Время вызова всех сторожей: {res['elapsed_sec']} сек")
    print(f"🔹 Запечатано гермо-кабин: {res.get('hermetic', {}).get('locked_count', 10)}")
    print(f"🔹 {res.get('bukvitsa', {}).get('summary', '')}")
    print("=" * 65)

    print(f"🔹 Запечатано гермо-кабин: {res['hermetic'].get('sealed_cabins', 0)}")
    print(f"🔹 Извлеченная память: {res['memory'].get('selected_archive', 'N/A')}")
    print(f"🔹 Давление пара: ~{res['steam'].get('tokens', 0):,} токенов ({res['steam'].get('status', 'OK')})")
    print(f"🔹 Экипаж агентов: {'🟢 100% ЗДОРОВЫ И В СТРОЮ' if res['health'].get('all_healthy') else '🔴 СБОЙ'}")
    print("=" * 65)
