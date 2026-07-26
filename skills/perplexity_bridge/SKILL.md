---
name: perplexity-bridge
description: Automates generation of search queries, prompt formatting, and data extraction from Perplexity Pro through browser session cookies or manual copy-paste handshakes. Use this skill when the user asks to search for new packages, libraries, or GitHub code templates.
---

# 📡 Skill: Perplexity Pro Bridge (Штурман)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


This skill governs how the Brigadier interfaces with Perplexity Pro to gather external information, templates, and libraries from the web.

## 1. Trigger Conditions
Activate this skill when:
- We need to find an existing GitHub repository, code library, or configuration sample.
- The user requests a web search that requires deep analytical synthesis rather than simple factual lookup.
- We need to double-check error codes or documentation for external APIs.

## 2. Modes of Operation

### Mode A: WebSocket Automation (Autopilot)
If Chrome remote debugging is active:
1. Ensure Google Chrome is closed and restarted cleanly with the debugging port enabled:
   `killall "Google Chrome" ; sleep 2 ; "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/Users/tur/Desktop/notebook_lm_school/chrome_profile" &`
2. Run the automation python script to input search prompt and wait for answer:
   `python perplexity_runner.py "<YOUR_QUERY>"`
3. The script inputs text using selection range simulation, submits via KeyboardEvent Enter, and polls for streaming text stability.
4. Extract the answer block output from the script and save it to the `05_ИССЛЕДОВАНИЯ` folder.

### Mode B: Human Handshake (Manual Sync)
If browser automation is blocked by OS or Captchas:
1. Generate a structured, formatted prompt based on the template in `[01_ДНК] Инструкция для Perplexity Pro.txt`.
2. Present the prompt to the user in a clean code block.
3. Prompt the user: "Copy this query into Perplexity Pro in your browser, then paste the full output here."
4. Process the pasted markdown output on the local workspace.