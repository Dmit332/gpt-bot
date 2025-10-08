# 🎯 Готовые JSON файлы для импорта в n8n

## ✅ Все workflows готовы к импорту!

Я создал 6 готовых JSON файлов в формате n8n, которые можно импортировать **одним кликом**.

---

## 📦 Список файлов

### 1️⃣ **n8n_workflow_1_new_lead.json**
**Название:** Новый лид - Автоматическая обработка  
**Что делает:**
- Принимает webhook с данными лида
- Создает клиента в CRM через MCP
- Отправляет приветственное сообщение в WhatsApp
- Возвращает результат

**Webhook URL:** `/webhook/new-lead`

**Тестовый запрос:**
```bash
curl -X POST http://localhost:5678/webhook/new-lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "website",
    "preferences": {"type": "apartment"}
  }'
```

---

### 2️⃣ **n8n_workflow_2_property_search.json**
**Название:** Автоподбор объектов по предпочтениям  
**Что делает:**
- Получает предпочтения клиента
- Обновляет их в CRM
- Ищет подходящие объекты
- Форматирует красивую подборку
- Отправляет в WhatsApp

**Webhook URL:** `/webhook/search-properties`

**Тестовый запрос:**
```bash
curl -X POST http://localhost:5678/webhook/search-properties \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client_123",
    "phone": "+79991234567",
    "preferences": {
      "type": "apartment",
      "max_price": 5000000,
      "rooms": 2
    }
  }'
```

---

### 3️⃣ **n8n_workflow_3_content_schedule.json**
**Название:** Публикация контента по расписанию  
**Что делает:**
- Запускается каждые 12 часов (настраивается)
- Получает расписание контента
- Фильтрует контент на сегодня
- Форматирует посты с хэштегами
- Отмечает опубликованным

**Расписание:** Каждые 12 часов (cron: `0 */12 * * *`)

---

### 4️⃣ **n8n_workflow_4_whatsapp_ai.json**
**Название:** WhatsApp - AI обработка сообщений  
**Что делает:**
- Принимает входящие сообщения от Twilio
- Парсит данные WhatsApp
- Отправляет в AI-ассистента
- Получает умный ответ
- Отправляет обратно клиенту

**Webhook URL:** `/webhook/whatsapp-incoming`

**Настройка в Twilio:**
```
Twilio Console → WhatsApp → Sandbox Settings
"When a message comes in": http://your-domain:5678/webhook/whatsapp-incoming
```

---

### 5️⃣ **n8n_workflow_5_content_pack.json**
**Название:** Генерация контент-пакета на месяц  
**Что делает:**
- Запускается 1-го числа каждого месяца в 9:00
- Генерирует 10 постов + 15 сторис
- Формирует отчет
- Отправляет уведомление в Telegram

**Расписание:** 1-го числа в 9:00 (cron: `0 9 1 * *`)

---

### 6️⃣ **n8n_workflow_6_hot_leads.json**
**Название:** Уведомления о горячих лидах  
**Что делает:**
- Принимает webhook о статусе лида
- Проверяет квалификацию (status = "qualified")
- Получает полные данные клиента
- Форматирует красивый алерт
- Отправляет менеджеру в Telegram

**Webhook URL:** `/webhook/hot-lead`

**Тестовый запрос:**
```bash
curl -X POST http://localhost:5678/webhook/hot-lead \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client_123",
    "status": "qualified"
  }'
```

---

## 🚀 Быстрый импорт

### Способ 1: Импорт из файла (рекомендуется)

1. Откройте n8n: `http://localhost:5678`
2. Нажмите **"+"** (новый workflow)
3. Нажмите **"..."** (три точки) → **"Import from File"**
4. Выберите файл `n8n_workflow_1_new_lead.json`
5. Нажмите **"Save"**
6. Повторите для всех 6 файлов

### Способ 2: Импорт через clipboard

1. Откройте файл `n8n_workflow_1_new_lead.json` в редакторе
2. Скопируйте весь JSON (Ctrl+A → Ctrl+C)
3. В n8n: **"..."** → **"Import from Clipboard"**
4. Вставьте JSON
5. Нажмите **"Import"**

---

## ⚙️ Настройка после импорта

### 1. Измените URL API сервера

В каждом HTTP Request ноде измените:
```
http://localhost:5000 → http://your-domain.com
```

Или если n8n в Docker:
```
http://localhost:5000 → http://host.docker.internal:5000
```

### 2. Добавьте переменные окружения

**Settings → Environment Variables:**
```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_MANAGER_CHAT_ID = your_chat_id
```

**Как получить:**
- Token: @BotFather в Telegram
- Chat ID: @userinfobot в Telegram

### 3. Активируйте workflows

Для каждого workflow:
- Откройте workflow
- Переключатель справа вверху: **Inactive → Active**

---

## 🧪 Тестирование

### Тест Workflow 1 (Новый лид):
```bash
curl -X POST http://localhost:5678/webhook/new-lead \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "phone": "+79999999999", "channel": "test"}'
```

### Тест Workflow 2 (Поиск):
```bash
curl -X POST http://localhost:5678/webhook/search-properties \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test_001", 
    "phone": "+79999999999",
    "preferences": {"type": "apartment", "max_price": 5000000}
  }'
```

### Тест Workflow 6 (Горячий лид):
```bash
curl -X POST http://localhost:5678/webhook/hot-lead \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test_001", "status": "qualified"}'
```

---

## 📊 Структура каждого workflow

### Общая структура:
```
Trigger (Webhook/Schedule)
    ↓
HTTP Request (MCP/API)
    ↓
Code (Обработка данных)
    ↓
HTTP Request (Отправка результата)
    ↓
Response/Log
```

### Используемые типы нодов:
- **Webhook** - прием данных
- **Schedule Trigger** - расписание
- **HTTP Request** - запросы к API
- **Code** - JavaScript обработка
- **If** - условия
- **Respond to Webhook** - ответы

---

## 🔧 Кастомизация

### Изменить расписание (Workflow 3, 5):

1. Откройте нод "Schedule Trigger"
2. Измените cron expression:
   - Каждые 6 часов: `0 */6 * * *`
   - Каждый день в 10:00: `0 10 * * *`
   - Каждый понедельник: `0 9 * * 1`

### Изменить логику форматирования:

1. Откройте Code нод
2. Измените JavaScript код
3. Сохраните

### Добавить новые действия:

1. Перетащите новый нод из левого меню
2. Подключите к существующим
3. Настройте параметры

---

## 📋 Чек-лист импорта

**Перед импортом:**
- [ ] n8n установлен и запущен (`n8n start`)
- [ ] API сервер работает (`python api_server.py`)
- [ ] WhatsApp бот работает (опционально)

**После импорта:**
- [ ] Все 6 workflows импортированы
- [ ] URL изменены на ваш домен
- [ ] Переменные окружения добавлены
- [ ] Workflows активированы (Active)
- [ ] Webhook URLs протестированы

---

## 🎯 Webhook URLs (после активации)

```
1. Новый лид:        http://localhost:5678/webhook/new-lead
2. Поиск объектов:   http://localhost:5678/webhook/search-properties
3. (Schedule - нет webhook)
4. WhatsApp:         http://localhost:5678/webhook/whatsapp-incoming
5. (Schedule - нет webhook)
6. Горячий лид:      http://localhost:5678/webhook/hot-lead
```

Замените `localhost:5678` на ваш домен в продакшене!

---

## 💡 Советы

### Production:
- Используйте HTTPS для webhooks
- Добавьте аутентификацию в n8n
- Включите error handling
- Настройте retry логику

### Monitoring:
- Проверяйте Executions в n8n
- Используйте логирование
- Настройте алерты при ошибках

### Оптимизация:
- Кешируйте частые запросы
- Используйте batch операции
- Оптимизируйте расписания

---

## 🆘 Troubleshooting

### "Connection refused"
→ Проверьте что API сервер запущен  
→ Измените URL на правильный  
→ Для Docker используйте `host.docker.internal`

### "Webhook not found"
→ Активируйте workflow  
→ Подождите 2-3 секунды  
→ Обновите страницу

### Telegram не работает
→ Добавьте переменные окружения  
→ Проверьте токен в @BotFather  
→ Проверьте Chat ID

---

## 📚 Дополнительно

**Полная документация:**
- `N8N_IMPORT_GUIDE.md` - Подробная инструкция
- `README.md` - Описание системы
- `MCP_REFERENCE.md` - API справочник
- `MCP_N8N_TOOLS_LIST.md` - Список инструментов

**Примеры использования:**
```bash
python example_usage.py  # Запустить все примеры
```

---

## ✅ Готово!

Все 6 workflows готовы к использованию!

**Следующие шаги:**
1. ✅ Импортируйте workflows в n8n
2. ✅ Настройте URL и переменные
3. ✅ Активируйте workflows
4. ✅ Протестируйте через curl
5. ✅ Начните принимать лиды!

---

**Вопросы?** Смотрите `N8N_IMPORT_GUIDE.md` для подробной инструкции!

🎉 **Успешной автоматизации!**
