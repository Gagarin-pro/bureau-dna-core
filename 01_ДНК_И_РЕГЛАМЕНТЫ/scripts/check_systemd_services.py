#!/usr/bin/env python3
import paramiko
import sys

ip = "216.57.106.146"
user = "root"
password = "d6X5-1bhgoK_Kj"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=ip, username=user, password=password, timeout=10)
    
    # Check all active systemd services
    stdin, stdout, stderr = client.exec_command("systemctl list-units --type=service --state=running | grep -E 'monolith|bot|backend|node|pm2'")
    output = stdout.read().decode('utf-8')
    
    # Check PM2 processes (since Node.js projects often use PM2)
    stdin, stdout, stderr = client.exec_command("pm2 list 2>/dev/null || echo 'pm2 not installed'")
    pm2_output = stdout.read().decode('utf-8')

    # Check running processes with ps aux
    stdin, stdout, stderr = client.exec_command("ps aux | grep -E 'node|index.js|server.js|bot.js|main.py'")
    ps_output = stdout.read().decode('utf-8')
    
    print("--- SYSTEMD RUNNING SERVICES (matching filter) ---")
    print(output if output.strip() else "No matching systemd services running.")
    
    print("\n--- PM2 PROCESS LIST ---")
    print(pm2_output.strip())
    
    print("\n--- PROCESS LIST (grep node/python/js) ---")
    print(ps_output.strip())
        
except Exception as e:
    print(f"🔴 Ошибка подключения: {e}", file=sys.stderr)
finally:
    client.close()
