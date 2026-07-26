import os
import re

def parse_frontmatter(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            yaml_block = match.group(1)
            name_match = re.search(r'^name:\s*(.+)$', yaml_block, re.MULTILINE)
            desc_match = re.search(r'^description:\s*(.+)$', yaml_block, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else os.path.basename(os.path.dirname(file_path))
            desc = desc_match.group(1).strip() if desc_match else ""
            return name, desc
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return None, None

def scan_skills():
    home = os.path.expanduser("~")
    search_dirs = [
        os.path.join(home, ".gemini/config/plugins/"),
        os.path.join(home, ".gemini/antigravity/builtin/skills/"),
        os.path.join(home, "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/.agents/skills/")
    ]
    skills = []
    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            if "SKILL.md" in files:
                full_path = os.path.join(root, "SKILL.md")
                name, desc = parse_frontmatter(full_path)
                if name:
                    skills.append({
                        "name": name,
                        "path": full_path,
                        "description": desc
                    })
    return skills

def main():
    skills = scan_skills()
    skills.sort(key=lambda x: x["name"])
    
    home = os.path.expanduser("~")
    output_path = os.path.join(home, "Desktop/ИИ_ОКРУЖЕНИЕ/AgentBrain/05-Meta/КАРТОТЕКА_НАВЫКОВ_ИИ.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 🗂️ КАРТОТЕКА КОГНИТИВНЫХ НАВЫКОВ ИИ-БРИГАДИРА\n")
        f.write(f"> **Статус:** Активна | Всего загружено навыков: {len(skills)}\n")
        f.write("> **Автоматизация:** Сканируется ежедневно в 9:00 через Compute Engine GCP\n\n")
        f.write("---\n\n")
        f.write("## 🛠️ СПИСОК ПОДКЛЮЧЕННЫХ УМЕНИЙ (SKILLS)\n\n")
        f.write("| Название навыка | Описание / Назначение | Локальный физический адрес |\n")
        f.write("| :--- | :--- | :--- |\n")
        for s in skills:
            # Mask paths for clean visibility
            clean_path = s["path"].replace("/Users/tur/Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»", "[Workspace]")
            clean_path = clean_path.replace("/Users/tur/.gemini/", "[Global]")
            f.write(f"| **{s['name']}** | {s['description']} | `{clean_path}` |\n")
            
    print(f"[+] Картотека успешно обновлена: {output_path} (Найдено: {len(skills)} навыков)")

if __name__ == "__main__":
    main()
