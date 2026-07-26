import urllib.request
import json
import os

def fetch_github_skills(query="agentic skills OR mcp server OR multi-agent framework"):
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity-Agent'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])
            results = []
            for item in items[:10]: # Top 10 repositories
                results.append({
                    "name": item.get("full_name") or item.get("name"),
                    "url": item.get("html_url"),
                    "description": item.get("description") or "Нет описания."
                })
            return results
    except Exception as e:
        print(f"Error fetching GitHub skills: {e}")
    return []

def main():
    import sys
    query = "google gemini OR google antigravity OR google ai studio OR agentic skills OR multi-agent framework"
    if len(sys.argv) > 1 and sys.argv[1].strip():
        query = " ".join(sys.argv[1:])
        
    print(f"[*] Запуск разведки самосовершенствования ИИ, Google AI и внешних умений по запросу: {query}...")
    repos = fetch_github_skills(query)
    
    home = os.path.expanduser("~")
    output_path = os.path.join(home, "Desktop/ИИ_ОКРУЖЕНИЕ/AgentBrain/05-Meta/КАРТОТЕКА_НАВЫКОВ_ИИ.md")
    if not os.path.exists(output_path):
        print(f"[-] Файл картотеки не найден: {output_path}")
        return
        
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    split_marker = "## 🌍 РЕКОМЕНДУЕМЫЕ ВНЕШНИЕ УМЕНИЯ (GITHUB)"
    if split_marker in content:
        content = content.split(split_marker)[0]
        
    new_section = f"{split_marker}\n"
    new_section += f"> **Разведка самосовершенствования ИИ и релизов Google AI:** Автоматическое отслеживание новшеств Gemini 3.6+, Antigravity SDK, MCP-серверов и мульти-агентных систем.\n\n"
    new_section += "| Репозиторий / Инструмент | Назначение / Полезность для ИИ-Архитектора | Ссылка на чертежи |\n"
    new_section += "| :--- | :--- | :--- |\n"
    
    if repos:
        for r in repos[:7]:
            new_section += f"| **{r['name']}** | {r['description']} | [{r['url']}]({r['url']}) |\n"
    else:
        new_section += "| **Очередь пуста** | Новых репозиториев не обнаружено | - |\n"
        
    updated_content = content.strip() + "\n\n" + new_section
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
        
    print(f"[+] Глобальная разведка завершена. Обновлен отчет в {output_path}")

if __name__ == "__main__":
    main()
