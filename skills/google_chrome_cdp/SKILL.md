---
name: google-chrome-cdp
description: Автоматизация Google Chrome через протокол CDP (Chrome DevTools Protocol) на порту 9222. Управление страницами, клики, ввод текста, скроллинг и снятие скриншотов в веб-сервисах (Google Vids, Google Drive и др.).
---

# 🤖 УМЕНИЕ: АВТОМАТИЗАЦИЯ GOOGLE CHROME (CDP BRIDGE)

> ⚡ **СТАНДАРТ БЮРО LEGO-ARCHITECT PRO**:
> 1. **Закон Атомарности (`atomic-batch-executor`)**: Выполнять чтение и запись файлов исключительно параллельными пакетными вызовами (экономия 50% топлива).
> 2. **Закон Сверх-Сжатого Левого Вакуума**: Выгружать развернутые логи и отчеты ИСКЛЮЧИТЕЛЬНО в `РАБОЧИЙ_ДИАЛОГ.md` (ограничение UI до 15 токенов).


Это умение активируется при необходимости управлять браузером Google Chrome, автоматизировать действия в Google Workspace (Vids, Docs, Диск) или выполнять веб-интеракции через протокол отладки.

---

## 🧭 1. ФИЗИЧЕСКИЙ ОБРАЗ (АНАЛОГИЯ)
Управление браузером через CDP — это **«цифровой пульт управления с лазерным наведением»**. Вместо того чтобы просить пользователя нажимать кнопки на экране («синдром водопроводчика»), ИИ-Архитектор использует «невидимую руку» для перемещения мыши, нажатия клавиш и считывания показаний приборов (скриншоты).

---

## ⚡ 2. ПОДКЛЮЧЕНИЕ И ПОИСК ТАРГЕТА
Браузер запускается пользователем с флагом удаленной отладки:
`--remote-debugging-port=9222`

### Шаблон подключения на Python (нахождение нужной вкладки):
```python
import json
import urllib.request
import websockets
import sys

def get_websocket_url(url_substring="/videos/"):
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json")
        with urllib.request.urlopen(req) as response:
            tabs = json.loads(response.read().decode())
        for tab in tabs:
            url = tab.get("url", "")
            if tab.get("type") == "page" and url_substring in url:
                return tab["webSocketDebuggerUrl"]
    except Exception as e:
        print(f"[-] Не удалось подключиться к порту 9222: {e}")
        sys.exit(1)
    print(f"[-] Вкладка с '{url_substring}' не найдена.")
    sys.exit(1)
```

---

## 🛠️ 3. ОСНОВНЫЕ КОМАНДЫ УПРАВЛЕНИЯ (ПРОТОКОЛ CDP)

### А. Выполнение JavaScript (`Runtime.evaluate`):
Используется для чтения DOM, ввода текста и поиска элементов.
```python
async def run_js(ws, expression, context_id=1):
    payload = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "returnByValue": True,
            "contextId": context_id
        }
    }
    await ws.send(json.dumps(payload))
    # Чтение ответа...
```

### Б. Снятие скриншота экрана (`Page.captureScreenshot`):
Всегда возвращайте скриншот для визуального подтверждения (ОТК).
*Важно:* Чтобы избежать ошибки превышения размера фрейма websockets (1009 Frame Exceeds Limit), подключайтесь с параметром `max_size=20*1024*1024` (20 МБ).
```python
async def capture_screen(ws, filepath):
    payload = {"id": 9999, "method": "Page.captureScreenshot", "params": {"format": "png"}}
    await ws.send(json.dumps(payload))
    # Сохранение base64 данных в файл...
```

### В. Физический прицельный клик (`Input.dispatchMouseEvent`):
Если обычный `.click()` в JS не срабатывает из-за оверлеев или кастомных фреймворков (Wiz, Angular, React), используйте физические координаты:
```python
async def click_coordinates(ws, x, y):
    # MousePressed
    await ws.send(json.dumps({
        "method": "Input.dispatchMouseEvent",
        "params": {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1}
    }))
    await asyncio.sleep(0.1)
    # MouseReleased
    await ws.send(json.dumps({
        "method": "Input.dispatchMouseEvent",
        "params": {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1}
    }))
```

---

## ⚠️ 4. ЗОЛОТЫЕ ПРАВИЛА И ПРЕДОХРАНИТЕЛИ (БЕЗБАГОВЫЙ КОД)

1.  **Защита SVG-элементов:** При разборе классов в JS всегда приводите `className` к строке или проверяйте тип. `className.includes` вызывает критическую ошибку на SVG-элементах (где `className` является объектом `SVGAnimatedString`).
    *Правильно:*
    ```javascript
    let cls = (typeof el.className === 'string') ? el.className : (el.className && el.className.animVal ? el.className.animVal : '');
    ```
2.  **Предварительный скроллинг:** Перед получением координат кнопки обязательно выполните скроллинг в центр экрана:
    ```javascript
    btn.scrollIntoView({block: 'center'});
    ```
    Затем подождите 1 секунду завершения анимации прокрутки, считайте новые координаты через `getBoundingClientRect()` и только тогда производите CDP-клик.
3.  **Асинхронные паузы:** После ввода текста или клика на генерацию ИИ по сценарию давайте интерфейсу паузу (от 5 до 20 секунд) на отправку сетевых запросов и отрисовку состояний перед снятием скриншота.

## ⚠️ 5. ТРАБЛШУТИНГ И УПРАВЛЕНИЕ ЗАПУСКОМ НА MAC (CHROME & CDP BOOT)

### А. Ошибка "Connection Refused" (Порт 9222 закрыт)
Если Chrome не запущен с флагом отладки, скрипты упадут с ошибкой подключения.
- **Действие:** Запустите Chrome на Mac принудительно через терминал:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/Users/tur/Desktop/notebook_lm_school/chrome_profile" --no-first-run &`
- **Проверка порта:** Убедитесь, что порт активен:
  `lsof -i :9222`

### Б. Ошибка "Address already in use" (Порт занят)
Если другой процесс занял порт 9222 (например, зависший фоновый инстанс Chrome Headless):
- **Решение:** Найдите PID процесса и убейте его:
  `kill -9 $(lsof -t -i:9222) 2>/dev/null || true`

### В. Автоматическая активация и фокус вкладок (Target.activateTarget)
Чтобы переключить визуальный фокус Chrome на нужный сервис (например, Google AI Studio или Google Flow) на экране Юрия:
```python
async def focus_tab(ws, target_id):
    payload = {
        "id": 2,
        "method": "Target.activateTarget",
        "params": {
            "targetId": target_id
        }
    }
    await ws.send(json.dumps(payload))
```
- **Как получить targetId:** Вызовите `http://127.0.0.1:9222/json` и найдите вкладку по URL.

### Г. Обход засыпания Chrome (Bonjour & Power Save)
На macOS Chrome в фоновом режиме может снижать приоритет CPU для неактивных вкладок, что вызывает тайм-ауты в CDP.
- **Решение:** Отключайте режим энергосбережения в настройках Chrome или посылайте регулярный холостой пинг `Runtime.evaluate(expression="1+1")` каждые 30 секунд для поддержания активности вкладки.
