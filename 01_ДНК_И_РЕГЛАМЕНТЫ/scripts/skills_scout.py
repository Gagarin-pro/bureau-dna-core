import urllib.request
import json
import os

def fetch_github_skills(query="antigravity+topic:ai-agents"):
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity-Agent'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])
            results = []
            for item in items[:10]: # Top 10 repositories
                results.append({
                    "name": item.get("name"),
                    "url": item.get("html_url"),
                    "description": item.get("description") or "Нет описания."
                })
            return results
    except Exception as e:
        print(f"Error fetching GitHub skills: {e}")
    return []

def main():
    import sys
    query = "antigravity topic:ai-agents"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        
    print(f"[*] Запуск глобальной разведки внешних умений по запросу: {query}...")
    repos = fetch_github_skills(query)
    
    home = os.path.expanduser("~")
    output_path = os.path.join(home, "Desktop/ИИ_ОКРУЖЕНИЕ/AgentBrain/05-Meta/КАРТОТЕКА_НАВЫКОВ_ИИ.md")
    if not os.path.exists(output_path):
        print(f"[-] Файл картотеки не найден: {output_path}")
        return
        
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content at external section if exists, or append
    split_marker = "## 🌍 РЕКОМЕНДУЕМЫЕ ВНЕШНИЕ УМЕНИЯ (GITHUB)"
    if split_marker in content:
        content = content.split(split_marker)[0]
        
    new_section = f"{split_marker}\n"
    new_section += f"> **Последняя разведка:** {urllib.request.urlopen('https://api.github.com').headers.get('Date') or 'Сегодня'}\n\n"
    new_section += "| Название репозитория | Описание | Ссылка на чертежи |\n"
    new_section += "| :--- | :--- | :--- |\n"
    
    if repos:
        for r in repos:
            new_section += f"| **{r['name']}** | {r['description']} | [{r['url']}]({r['url']}) |\n"
    else:
        new_section += "| **Очередь пуста** | Новых репозиториев не обнаружено | - |\n"
        
    updated_content = content.strip() + "\n\n" + new_section
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
        
    print(f"[+] Глобальная разведка завершена. Обновлен отчет в {output_path}")

if __name__ == "__main__":
    main()
