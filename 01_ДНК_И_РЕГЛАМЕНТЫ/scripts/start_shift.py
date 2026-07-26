import os
import sys
import subprocess
import re
import json
import time
import glob

MASTER_DIR = "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»"
MASTER_TEMPLATE_PATH = "/Users/tur/.gemini/config/autonomous_bureau_dashboard_master.md"

if len(sys.argv) < 2:
    print("Usage: python3 start_shift.py <brain_folder_path> [CABIN_NAME]")
    sys.exit(1)

brain_folder = sys.argv[1]
target_cabin_arg = sys.argv[2].upper() if len(sys.argv) > 2 else None
if not os.path.exists(brain_folder):
    print(f"Error: Brain folder {brain_folder} does not exist.")
    sys.exit(1)

print("Starting shift diagnostics...")

# -1. UPSTREAM PUSH SAFEGUARD (Защита от отката Ошибки №4)
try:
    drive_caravan_dir = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН")
    files_to_sync = ["РАБОЧИЙ_ДИАЛОГ.md", "ПОВЕСТКА_ПЛАНЕРКИ.md", "autonomous_bureau_dashboard.md", "АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md"]
    for f_name in files_to_sync:
        b_path = os.path.join(brain_folder, f_name)
        d_path = os.path.join(drive_caravan_dir, f_name)
        if os.path.exists(b_path):
            if not os.path.exists(d_path) or os.path.getmtime(b_path) >= os.path.getmtime(d_path):
                import shutil
                shutil.copy2(b_path, d_path)
except Exception as e:
    print(f"Warning: Upstream push safeguard error: {e}")

# 0. Read active cabin early if available
active_cabin_early = "МАСТЕР_КАБИНА"
active_cabin_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ACTIVE_CABIN.txt")
if len(sys.argv) > 2 and sys.argv[2].strip():
    active_cabin_early = sys.argv[2].strip().upper()
elif os.path.exists(active_cabin_path):
    try:
        with open(active_cabin_path, "r", encoding="utf-8") as f:
            v = f.read().strip().upper()
            if v and v != "NEUTRAL":
                active_cabin_early = v
    except Exception:
        pass

# 0. Run Unified Bureau Guards Engine (unified_guards_runner.py)
try:
    unified_runner = "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/scripts/unified_guards_runner.py"
    if os.path.exists(unified_runner):
        subprocess.run([sys.executable, unified_runner, brain_folder, active_cabin_early], check=False)
except Exception as e:
    print(f"Warning: Failed to run unified guards runner: {e}")

# 1. Check if gagarin_bridge is running
bridge_running = False
try:
    ps_out = subprocess.check_output("ps aux | grep gagarin_bridge | grep -v grep", shell=True).decode("utf-8")
    if "gagarin_bridge.py" in ps_out:
        bridge_running = True
except Exception:
    pass

# Auto-start Gagarin Bridge if not running
if not bridge_running:
    print("Gagarin Bridge is offline. Launching automatically in background...")
    try:
        venv_python = "/Users/tur/Desktop/ИИ_ОКРУЖЕНИЕ/notebook_lm_school/.venv/bin/python3"
        script_path = "/Users/tur/Desktop/ИИ_ОКРУЖЕНИЕ/notebook_lm_school/gagarin_bridge_v2/gagarin_bridge.py"
        if os.path.exists(venv_python) and os.path.exists(script_path):
            subprocess.Popen([venv_python, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            time.sleep(1.5)  # Wait for process initialization
            
            # Re-check running status
            ps_out = subprocess.check_output("ps aux | grep gagarin_bridge | grep -v grep", shell=True).decode("utf-8")
            if "gagarin_bridge.py" in ps_out:
                bridge_running = True
                print("Gagarin Bridge successfully started!")
        else:
            print("Error: Gagarin executable or script path not found.")
    except Exception as e:
        print(f"Failed to auto-start Gagarin Bridge: {e}")

bridge_status = "🟢 Активен" if bridge_running else "🔴 Неактивен"
bridge_desc = "Go (Соединение стабильно)" if bridge_running else "Остановлен (Не удалось запустить)"

# 2. Check n8n cloud status
caddy_running = False
try:
    code_http = subprocess.check_output('curl -k -s -o /dev/null -w "%{http_code}" https://35.229.90.22/ --connect-timeout 3', shell=True).decode("utf-8").strip()
    if code_http in ["200", "302", "404", "401"]:
        caddy_running = True
except Exception:
    pass

n8n_status = "🟢 Активен" if caddy_running else "🔴 Неактивен"
n8n_desc = "Go (Шлюз SSL Caddy активен)" if caddy_running else "Недоступен"

# 3. Calculate boiler pressure (tokens) dynamically using steam_pressure_monitor.py
pressure_tokens = 0
pressure_status = "🟢 Ледяной режим"
pressure_desc = "Замер в норме"
try:
    pressure_script_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/scripts/steam_pressure_monitor.py")
    if os.path.exists(pressure_script_path):
        pressure_out = subprocess.check_output(f"python3 '{pressure_script_path}' '{brain_folder}'", shell=True).decode("utf-8")
        tokens_match = re.search(r"Живой объем пара в токенах: ~([\d,]+) токенов \((\d+\.\d+)%", pressure_out)
        if tokens_match:
            pressure_tokens = int(tokens_match.group(1).replace(",", ""))
            pressure_pct = float(tokens_match.group(2))
            
            if "🔴 КРАСНАЯ ЗОНА" in pressure_out:
                pressure_status = "🔴 ПЕРЕХОД"
                pressure_desc = f"~{pressure_tokens:,} токенов ({pressure_pct}% / ПОРОГ ПЕРЕХОДА)".replace(",", " ")
            elif "🟧 Предупредительная зона" in pressure_out:
                pressure_status = "🟧 Предупреждение"
                pressure_desc = f"~{pressure_tokens:,} токенов ({pressure_pct}% / Нагрев котлов)".replace(",", " ")
            else:
                pressure_status = "🟢 Ледяной режим"
                pressure_desc = f"~{pressure_tokens:,} токенов ({pressure_pct}% / Ледяной режим)".replace(",", " ")
                
        # Run steam_guard.py to check for automatic bridge assembly
        guard_script_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/scripts/steam_guard.py")
        if os.path.exists(guard_script_path):
            subprocess.Popen([sys.executable, guard_script_path, brain_folder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
except Exception as e:
    pressure_desc = f"Ошибка датчика: {e}"

# 4. Count active skills and launch external scout in background
skills_count = 0
try:
    search_dirs = [
        os.path.join(os.path.expanduser("~"), ".gemini/config/plugins/"),
        os.path.join(os.path.expanduser("~"), ".gemini/config/skills/"),
        os.path.join(os.path.expanduser("~"), ".gemini/antigravity/builtin/skills/"),
        os.path.join(MASTER_DIR, ".agents/skills/")
    ]
    unique_skills = set()
    for base_dir in search_dirs:
        if os.path.exists(base_dir):
            for root, dirs, files in os.walk(base_dir):
                if "SKILL.md" in files:
                    # Добавляем имя папки как имя уникального навыка
                    unique_skills.add(os.path.basename(root))
    skills_count = len(unique_skills)

    # Автоматический фоновый запуск внешнего Скаута Умений
    scout_script = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/scripts/skills_scout.py")
    if os.path.exists(scout_script):
        subprocess.Popen([sys.executable, scout_script, "agentic skills"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print("Automatic background scout (skills_scout.py) launched successfully!")
except Exception as e:
    print(f"Warning: Failed to count skills or launch scout: {e}")


# 5. Read & Set Active Cabin + Copy Isolated NAVIGATOR.md
active_cabin = "МАСТЕР_КАБИНА"
active_cabin_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ACTIVE_CABIN.txt")

if target_cabin_arg:
    active_cabin = target_cabin_arg
    if active_cabin in ["BUREAU_SETUP", "MASTER_CABIN"]:
        active_cabin = "МАСТЕР_КАБИНА"
    try:
        with open(active_cabin_path, "w", encoding="utf-8") as cabin_f:
            cabin_f.write(active_cabin + "\n")
    except Exception as e:
        print(f"Warning: Failed to write active cabin: {e}")
else:
    try:
        if os.path.exists(active_cabin_path):
            with open(active_cabin_path, "r", encoding="utf-8") as cabin_f:
                val = cabin_f.read().strip().upper()
                if val and val != "NEUTRAL":
                    active_cabin = val
                    if active_cabin in ["BUREAU_SETUP", "MASTER_CABIN"]:
                        active_cabin = "МАСТЕР_КАБИНА"
    except Exception:
        pass

# Copy target cabin NAVIGATOR.md to brain folder
CABIN_DIRS = {
    "МАСТЕР_КАБИНА": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUREAU_SETUP": os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"),
    "BUKVITSA_BOT": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Буквица-бот",
    "MONOLITH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "MONOLITH_CEH": os.path.join(MASTER_DIR, "06_ЦЕХ_МОНОЛИТ"),
    "COURT_CASE": os.path.join(MASTER_DIR, "08_ЛИЧНЫЙ_КАРАВАН"),
    "AUTOSCHOOL": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "GAGARIN_OS": os.path.join(MASTER_DIR, "02_ЦЕХ_ГАГАРИН"),
    "AI_STUDIO_RD": "/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Google AI Studio — База R&D",
    "VPN_REALITY": os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ"),
}

CABIN_NAVIGATORS = {
    cname: (os.path.join(cdir, "NAVIGATOR.md") if cname not in ["BUREAU_SETUP", "МАСТЕР_КАБИНА"] else os.path.join(cdir, "СТАТУС_ПРОЕКТА.md"))
    for cname, cdir in CABIN_DIRS.items()
}

nav_src = CABIN_NAVIGATORS.get(active_cabin)
if nav_src and os.path.exists(nav_src):
    try:
        import shutil
        target_nav = os.path.join(brain_folder, "ACTIVE_CABIN_NAVIGATOR.md")
        shutil.copyfile(nav_src, target_nav)
        print(f"Isolated Cabin Navigator loaded: {nav_src} -> {target_nav}")
    except Exception as e:
        print(f"Warning: Failed to copy cabin navigator: {e}")

# 6. Read local files registry status
mac_registry_status = "⚪ Не сканировалась"
try:
    mac_reg_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/картотека_mac/КАРТОТЕКА_ФАЙЛОВ.md")
    if os.path.exists(mac_reg_path):
        mac_registry_status = "🟢 Активна (Файлы Mac)"
except Exception:
    pass

# 7. Parse active topic from ПОВЕСТКА_ПЛАНЕРКИ.md
active_topic = "Не определена"
try:
    agenda_path = os.path.join(brain_folder, "ПОВЕСТКА_ПЛАНЕРКИ.md")
    if not os.path.exists(agenda_path):
        agenda_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md")
    if os.path.exists(agenda_path):
        with open(agenda_path, "r", encoding="utf-8") as agenda_f:
            agenda_content = agenda_f.read()
            # Find the active topic indicated by ### [/]
            topic_match = re.search(r"### \[\/\]\s*(.*?)(?:\n|$)", agenda_content)
            if topic_match:
                active_topic = topic_match.group(1).strip()
except Exception as e:
    print(f"Warning: Failed to parse agenda: {e}")

if os.path.exists(MASTER_TEMPLATE_PATH):
    with open(MASTER_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        dashboard_content = f.read()
else:
    print(f"Error: Master template {MASTER_TEMPLATE_PATH} not found.")
    sys.exit(1)

lines = dashboard_content.splitlines()
for idx, line in enumerate(lines):
    if "Текущая Точка сборки:" in line:
        lines[idx] = f"*   **Текущая Точка сборки:** {active_topic}\n*   **Активная кабина проекта:** 🟢 {active_cabin}"
    elif "Давление в котлах (Длина чата)" in line:
        lines[idx] = f"| **Давление в котлах (Длина чата)** | {pressure_status} | Замер накопленного пара (объема текста диалога и файлов) | {pressure_desc} |"
    elif "Мост Гагарин (Mac ⇄ Облако)" in line:
        lines[idx] = f"| **Мост Гагарин (Mac ⇄ Облако)** | {bridge_status} | Фоновый мост связи файлов Mac с облачным сервером | {bridge_status} ({bridge_desc}) |"
    elif "Диспетчер автоматики (n8n)" in line:
        lines[idx] = f"| **Диспетчер автоматики (n8n)** | {n8n_status} | Облачный диспетчерский пункт на сервере GCP | {n8n_status} ({n8n_desc}) |"
    elif "Ревизор Картотеки" in line:
        lines[idx] = f"| **Ревизор Картотеки** | {mac_registry_status} | Датчик инвентаризации когнитивных умений | 🟢 {skills_count} уникальных умений активны |"
    elif "| `/audit` |" in line:
        lines[idx] = f"| `/audit` | Ревизия умений | Пересчет и обновление Картотеки умений ({skills_count} навыков) |"
    
    # Auto-update active/archived states for cabins
    cabin_match = re.search(r"^\*\s+([⚪🟢])\s+\*\*`(\w+)`\*\*\s+\[(Активна|Законсервирована)\]", line)
    if cabin_match:
        cabin_name = cabin_match.group(2)
        if cabin_name == active_cabin:
            line = re.sub(r"([⚪🟢])\s+(\*\*`" + cabin_name + r"`\*\*)\s+\[(Активна|Законсервирована)\]", r"🟢 \2 [Активна]", line)
        else:
            line = re.sub(r"([⚪🟢])\s+(\*\*`" + cabin_name + r"`\*\*)\s+\[(Активна|Законсервирована)\]", r"⚪ \2 [Законсервирована]", line)
        lines[idx] = line

updated_dashboard = "\n".join(lines) + "\n"

target_dashboard_path = os.path.join(brain_folder, "autonomous_bureau_dashboard.md")
with open(target_dashboard_path, "w", encoding="utf-8") as f:
    f.write(updated_dashboard)

dashboard_meta = {
    "UserFacing": True,
    "RequestFeedback": True,
    "Summary": "Автоматически откалиброванная приборная панель управления (версия 2.0). Диагностика систем завершена."
}
with open(target_dashboard_path + ".metadata.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_meta, f, indent=2, ensure_ascii=False)

def safe_copy(src, dst):
    if not os.path.exists(src):
        return False
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        import shutil
        shutil.copy2(src, dst)
        return True
    return False

active_cabin_dir = CABIN_DIRS.get(active_cabin, os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН"))
source_agenda_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md")
target_agenda_path = os.path.join(brain_folder, "ПОВЕСТКА_ПЛАНЕРКИ.md")

# Copy dedicated workshop agenda if present in cabin directory
source_ceh_agenda_path = os.path.join(active_cabin_dir, "ПОВЕСТКА_ЦЕХА.md")
target_ceh_agenda_path = os.path.join(brain_folder, "ПОВЕСТКА_ЦЕХА.md")
if os.path.exists(source_ceh_agenda_path):
    safe_copy(source_ceh_agenda_path, target_ceh_agenda_path)
    with open(target_ceh_agenda_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump({"UserFacing": True, "RequestFeedback": True, "Summary": "Локальная повестка активного цеха Бюро."}, f, indent=2, ensure_ascii=False)

# Copy isolated dialogue and agenda for active cabin
source_dialogue_path = os.path.join(active_cabin_dir, "РАБОЧИЙ_ДИАЛОГ.md")
target_dialogue_path = os.path.join(brain_folder, "РАБОЧИЙ_ДИАЛОГ.md")
if os.path.exists(source_dialogue_path):
    safe_copy(source_dialogue_path, target_dialogue_path)

if safe_copy(source_agenda_path, target_agenda_path):
    agenda_meta = {
        "UserFacing": True,
        "RequestFeedback": True,
        "Summary": "Повестка и решения планерки с КВС Юрием."
    }
    with open(target_agenda_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(agenda_meta, f, indent=2, ensure_ascii=False)

source_reg_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md")
target_reg_path = os.path.join(brain_folder, "АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md")
if safe_copy(source_reg_path, target_reg_path):
    reg_meta = {
        "UserFacing": True,
        "RequestFeedback": False,
        "Summary": "Утвержденный Мастер-Регламент Бюро Проектирования (версия 1.8)."
    }
    with open(target_reg_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(reg_meta, f, indent=2, ensure_ascii=False)

source_agents_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/КАРТОТЕКА_СУБАГЕНТОВ_БЮРО.md")
target_agents_path = os.path.join(brain_folder, "КАРТОТЕКА_СУБАГЕНТОВ_БЮРО.md")
if safe_copy(source_agents_path, target_agents_path):
    agents_meta = {
        "UserFacing": True,
        "RequestFeedback": False,
        "Summary": "Реестр специализированных ИИ-станков и роботов-помощников Автономного Бюро."
    }
    with open(target_agents_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(agents_meta, f, indent=2, ensure_ascii=False)

source_errors_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/ХРОНИКА_ОШИБОК.md")
target_errors_path = os.path.join(brain_folder, "ХРОНИКА_ОШИБОК.md")
if safe_copy(source_errors_path, target_errors_path):
    errors_meta = {
        "UserFacing": True,
        "RequestFeedback": False,
        "Summary": "Реестр зафиксированных аварий сборочного конвейера и системных заплат."
    }
    with open(target_errors_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(errors_meta, f, indent=2, ensure_ascii=False)

source_dialog_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md")
source_dash_path = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md")
source_agenda_master = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md")
# Sync РАБОЧИЙ_ДИАЛОГ.md, autonomous_bureau_dashboard.md, and ПОВЕСТКА_ПЛАНЕРКИ.md to all brain directories for Electron GUI consistency
all_brain_dirs = glob.glob("/Users/tur/.gemini/antigravity/brain/*")
for b_dir in all_brain_dirs:
    if os.path.isdir(b_dir):
        b_target_dialog = os.path.join(b_dir, "РАБОЧИЙ_ДИАЛОГ.md")
        b_target_dash = os.path.join(b_dir, "autonomous_bureau_dashboard.md")
        b_target_agenda = os.path.join(b_dir, "ПОВЕСТКА_ПЛАНЕРКИ.md")
        safe_copy(source_dialog_path, b_target_dialog)
        safe_copy(source_dash_path, b_target_dash)
        safe_copy(source_agenda_master, b_target_agenda)
        with open(b_target_dialog + ".metadata.json", "w", encoding="utf-8") as f:
            json.dump({"UserFacing": True, "RequestFeedback": True, "Summary": "Рабочий интерактивный диалог с КВС Юрием."}, f, indent=2, ensure_ascii=False)
        with open(b_target_agenda + ".metadata.json", "w", encoding="utf-8") as f:
            json.dump({"UserFacing": True, "RequestFeedback": True, "Summary": "Повестка и решения планерки с КВС Юрием."}, f, indent=2, ensure_ascii=False)

# Copy ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md
source_tempo_path = os.path.join(MASTER_DIR, "01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md")
target_tempo_path = os.path.join(brain_folder, "ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md")
if safe_copy(source_tempo_path, target_tempo_path):
    tempo_meta = {
        "UserFacing": True,
        "RequestFeedback": False,
        "Summary": "Правила взаимоконтроля, темпа и закон торможения."
    }
    with open(target_tempo_path + ".metadata.json", "w", encoding="utf-8") as f:
        json.dump(tempo_meta, f, indent=2, ensure_ascii=False)



# 8. Handling Transition Bridge (ПЕРЕХОДНЫЙ_МОСТ.md)
bridge_file_src = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН/ПЕРЕХОДНЫЙ_МОСТ.md")
bridge_file_tgt = os.path.join(brain_folder, "ПЕРЕХОДНЫЙ_МОСТ.md")
if os.path.exists(bridge_file_src):
    try:
        import shutil
        shutil.copy2(bridge_file_src, bridge_file_tgt)
        os.remove(bridge_file_src) # remove on drive to prevent repeat
        
        bridge_meta = {
            "UserFacing": True,
            "RequestFeedback": True,
            "Summary": "Когнитивный переходный мост. Считайте этот файл для продолжения диалога."
        }
        with open(bridge_file_tgt + ".metadata.json", "w", encoding="utf-8") as f:
            json.dump(bridge_meta, f, indent=2, ensure_ascii=False)
        print("Transition Bridge detected and moved to active context.")
    except Exception as e:
        print(f"Warning: Failed to process Transition Bridge: {e}")

# 9. Auto-fix SSH_AUTH_SOCK in mcp_config.json
try:
    mcp_config_path = "/Users/tur/.gemini/config/mcp_config.json"
    current_ssh_auth = os.environ.get("SSH_AUTH_SOCK")
    if current_ssh_auth and os.path.exists(mcp_config_path):
        with open(mcp_config_path, "r", encoding="utf-8") as mcp_f:
            mcp_data = json.load(mcp_f)
        
        docker_env = mcp_data.get("mcpServers", {}).get("docker", {}).get("env", {})
        if docker_env and docker_env.get("SSH_AUTH_SOCK") != current_ssh_auth:
            docker_env["SSH_AUTH_SOCK"] = current_ssh_auth
            with open(mcp_config_path, "w", encoding="utf-8") as mcp_f:
                json.dump(mcp_data, mcp_f, indent=2, ensure_ascii=False)
            print(f"Auto-fixed SSH_AUTH_SOCK in mcp_config.json to: {current_ssh_auth}")
except Exception as e:
    print(f"Warning: Failed to auto-fix SSH_AUTH_SOCK: {e}")

print("Shift diagnostics and dashboard setup completed successfully!")


NAV_FOOTER = """

---

[📟 ПУЛЬТ УПРАВЛЕНИЯ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/РАБОЧИЙ_ДИАЛОГ.md) | [🏢 АВТОНОМНОЕ БЮРО](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/03_БОРТОВОЙ_КАРАВАН/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛑 ПРАВИЛА ТЕМПА](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)
"""

def ensure_footer(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.rstrip().split("\n")
        new_lines = []
        for line in lines:
            if "[🏢 АВТОНОМНОЕ БЮРО]" in line or "[📟 ПУЛЬТ УПРАВЛЕНИЯ]" in line or "[💬 ДИАЛОГ]" in line or "[👑 МАСТЕР-КАБИНА]" in line:
                continue
            new_lines.append(line)
        
        current_footer = NAV_FOOTER
        if "/.gemini/antigravity/brain/" in filepath:
            folder = os.path.dirname(filepath)
            current_footer = f"\n\n---\n\n[📟 ПУЛЬТ УПРАВЛЕНИЯ](file://{folder}/autonomous_bureau_dashboard.md) | [💬 ДИАЛОГ](file://{folder}/РАБОЧИЙ_ДИАЛОГ.md) | [🏢 АВТОНОМНОЕ БЮРО](file://{folder}/АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md) | [📅 ПОВЕСТКА ПЛАНЕРКИ](file://{folder}/ПОВЕСТКА_ПЛАНЕРКИ.md) | [🛑 ПРАВИЛА ТЕМПА](file:///Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой%20диск/iT%20технологии/AI_Studio/Автошкола%20ИИ/«LEGO-ARCHITECT%20PRO»/01_ДНК_И_РЕГЛАМЕНТЫ/ПРАВИЛА_ВЗАИМОКОНТРОЛЯ_И_ТЕМПА.md) | [🛠️ КАРТОТЕКА УМЕНИЙ](file:///Users/tur/.gemini/config/plugins/lego-architect-plugin/skills/bureau-regulations/SKILL.md)\n"
            
        new_content = "\n".join(new_lines).rstrip() + current_footer
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

# 1. Apply footers FIRST to brain files
for fname in ["РАБОЧИЙ_ДИАЛОГ.md", "autonomous_bureau_dashboard.md", "АВТОНОМНОЕ_БЮРО_ПРОЕКТИРОВАНИЯ.md", "ПОВЕСТКА_ПЛАНЕРКИ.md"]:
    ensure_footer(os.path.join(brain_folder, fname))

# 2. Auto-sync generated dashboard, agenda & dialog back to Google Drive Caravan AND Active Cabin
try:
    import shutil
    drive_caravan = os.path.join(MASTER_DIR, "03_БОРТОВОЙ_КАРАВАН")
    active_cabin_dir = CABIN_DIRS.get(active_cabin, drive_caravan)
    
    shutil.copy2(target_dashboard_path, os.path.join(drive_caravan, "autonomous_bureau_dashboard.md"))
    
    dialog_src = os.path.join(brain_folder, "РАБОЧИЙ_ДИАЛОГ.md")
    if os.path.exists(dialog_src):
        # Copy ALWAYS to main Caravan (read by Electron GUI)
        shutil.copy2(dialog_src, os.path.join(drive_caravan, "РАБОЧИЙ_ДИАЛОГ.md"))
        # Copy ALWAYS to active cabin folder
        if active_cabin_dir and active_cabin_dir != drive_caravan and os.path.exists(active_cabin_dir):
            shutil.copy2(dialog_src, os.path.join(active_cabin_dir, "РАБОЧИЙ_ДИАЛОГ.md"))
        
        # Also update today's archive files to prevent cabin_memory_recall from restoring old state
        import datetime
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        caravan_archive = os.path.join(drive_caravan, "ДИАЛОГИ", f"{today_str}_РАБОЧИЙ_ДИАЛОГ.md")
        os.makedirs(os.path.dirname(caravan_archive), exist_ok=True)
        shutil.copy2(dialog_src, caravan_archive)
        if active_cabin_dir and active_cabin_dir != drive_caravan and os.path.exists(active_cabin_dir):
            cabin_archive = os.path.join(active_cabin_dir, "ДИАЛОГИ", f"{today_str}_РАБОЧИЙ_ДИАЛОГ.md")
            os.makedirs(os.path.dirname(cabin_archive), exist_ok=True)
            shutil.copy2(dialog_src, cabin_archive)
        
    agenda_src = os.path.join(brain_folder, "ПОВЕСТКА_ПЛАНЕРКИ.md")
    if os.path.exists(agenda_src):
        shutil.copy2(agenda_src, os.path.join(drive_caravan, "ПОВЕСТКА_ПЛАНЕРКИ.md"))
        if active_cabin_dir and active_cabin_dir != drive_caravan and os.path.exists(active_cabin_dir):
            shutil.copy2(agenda_src, os.path.join(active_cabin_dir, "ПОВЕСТКА_ПЛАНЕРКИ.md"))

    ceh_agenda_src = os.path.join(brain_folder, "ПОВЕСТКА_ЦЕХА.md")
    if os.path.exists(ceh_agenda_src) and active_cabin_dir != drive_caravan:
        shutil.copy2(ceh_agenda_src, os.path.join(active_cabin_dir, "ПОВЕСТКА_ЦЕХА.md"))

    memo_src = os.path.join(brain_folder, "ПАМЯТКА_КВС_ВАЙБ_КОДИНГ.md")
    if os.path.exists(memo_src):
        shutil.copy2(memo_src, os.path.join(drive_caravan, "ПАМЯТКА_КВС_ВАЙБ_КОДИНГ.md"))
except Exception as e:
    print(f"Warning: Failed to sync files to Google Drive: {e}")
