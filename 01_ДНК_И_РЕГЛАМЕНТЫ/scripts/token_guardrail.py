import os
import sys

def get_color_prefix(level):
    if level == "GREEN":
        return "\033[92m"  # Green
    elif level == "YELLOW":
        return "\033[93m"  # Yellow
    else:
        return "\033[91m"  # Red
        
def get_color_suffix():
    return "\033[0m"

def main():
    home = os.path.expanduser("~")
    
    # Path to memory trailer
    trailer_path = os.path.join(
        home, 
        "Library/CloudStorage/GoogleDrive-n3804590@gmail.com/Мой диск/iT технологии/AI_Studio/Автошкола ИИ/«LEGO-ARCHITECT PRO»/03_БОРТОВОЙ_КАРАВАН/ПРИЦЕП_ПАМЯТИ.md"
    )
    
    if not os.path.exists(trailer_path):
        print(f"[-] Файл памяти не найден по пути: {trailer_path}")
        sys.exit(1)
        
    try:
        with open(trailer_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[-] Ошибка чтения файла памяти: {e}")
        sys.exit(1)
        
    char_count = len(content)
    # 1 Russian character is roughly 0.4 tokens in modern LLM tokenizers
    est_tokens = int(char_count * 0.4)
    
    # Count blocks
    blocks = content.count("### 🟩 БЛОК")
    
    # Determine health status
    if est_tokens < 25000 and blocks <= 4:
        status = "GREEN"
        desc = "Все отлично. Давление в норме, когнитивный дрейф отсутствует."
    elif est_tokens < 50000 and blocks <= 8:
        status = "YELLOW"
        desc = "Внимание! Объем памяти растет. Рекомендуется плановое сжатие (Context-Slicing)."
    else:
        status = "RED"
        desc = "КРИТИЧЕСКИЙ УРОВЕНЬ! Контекст переполнен. Срочно перенесите старые блоки в архив ПРИЦЕП_ПАМЯТИ_FULL.md!"
        
    prefix = get_color_prefix(status)
    suffix = get_color_suffix()
    
    print("=======================================================")
    print("🚦 ДАТЧИК ТОПЛИВНОГО ПРЕДОХРАНИТЕЛЯ (TOKEN GUARDRAIL)")
    print("=======================================================")
    print(f"📄 Файл: ПРИЦЕП_ПАМЯТИ.md")
    print(f"📊 Размер: {char_count:,} символов")
    print(f"🔥 Примерный объем: {est_tokens:,} токенов")
    print(f"📦 Активные блоки: {blocks} блоков памяти")
    print(f"⚡ Статус датчика: {prefix}[{status}]{suffix}")
    print(f"🧭 Рекомендация: {desc}")
    print("=======================================================")
    
if __name__ == "__main__":
    main()
