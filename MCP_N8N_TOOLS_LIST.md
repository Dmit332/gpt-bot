# 🛠️ MCP N8N - Список всех инструментов

## 📋 Полный список доступных MCP инструментов для n8n

У вас есть полнофункциональная система AI-бота для недвижимости с интеграцией n8n. Вот что включено:

---

## 🎯 1. MCP Server (mcp_server.py)

**Основной сервер для интеграции с n8n**

### Доступные действия (Actions):

✅ **create_client** - Создание клиента в CRM  
✅ **update_preferences** - Обновление предпочтений клиента  
✅ **get_client** - Получение данных клиента  
✅ **add_property** - Добавление объекта недвижимости  
✅ **search_properties** - Умный поиск объектов по фильтрам  
✅ **create_content** - Создание контента (посты/сторис)  
✅ **get_content_schedule** - Получение расписания публикаций  

**Использование:**
```
POST http://localhost:5000/api/mcp
Body: {"action": "название_действия", "params": {...}}
```

---

## 🤖 2. AI-Ассистент (ai_assistant.py)

**Интеллектуальный помощник для работы с клиентами**

### Возможности:

✅ Естественный диалог с клиентами  
✅ Автоматическое извлечение предпочтений из текста  
✅ Умный подбор объектов  
✅ Персонализированные рекомендации  
✅ Поддержка истории разговоров  
✅ Работа через любой канал (WhatsApp, сайт, Telegram)  

**API:**
```
POST /api/chat
{
  "client_id": "...",
  "message": "Ищу квартиру...",
  "channel": "whatsapp"
}
```

---

## 📱 3. WhatsApp Bot (whatsapp_bot.py)

**Полная интеграция с WhatsApp Business через Twilio**

### Возможности:

✅ Прием входящих сообщений  
✅ Автоматические ответы через AI  
✅ Отправка сообщений клиентам  
✅ Массовые рассылки  
✅ Отправка фото объектов  

**Webhooks:**
- `POST /whatsapp/webhook` - Прием сообщений
- `POST /whatsapp/send` - Отправка сообщения
- `POST /whatsapp/broadcast` - Массовая рассылка

---

## 🌐 4. Веб-виджет (web_widget.html)

**Красивый чат-виджет для сайта**

### Возможности:

✅ Современный дизайн с градиентами  
✅ Адаптивная верстка (мобильные + десктоп)  
✅ Typing indicators  
✅ Плавные анимации  
✅ Интеграция одним файлом  
✅ Автоматическое подключение к API  

**Доступ:** `http://localhost:5000/widget`

---

## 🎨 5. Генератор контента (content_generator.py)

**AI-генерация контента для соцсетей через GPT-4**

### Возможности:

✅ Автоматическая генерация постов  
✅ Создание Stories для Instagram  
✅ Подборки объектов (ТОП-5, по теме и т.д.)  
✅ Посты с отзывами клиентов  
✅ Полезные советы по недвижимости  
✅ **Автоматический контент-пакет на месяц (10+ постов, 15+ сторис)**  

**API:**
```
POST /api/content/generate - Сгенерировать контент
POST /api/content/pack - Создать пакет на месяц
GET /api/content/schedule - Расписание публикаций
```

**Типы контента:**
- `property_showcase` - Презентация объекта
- `selection` - Подборка объектов
- `tips` - Полезные советы
- `success_story` - История успеха
- `review_post` - Пост с отзывом

---

## 🔄 6. N8N Workflows (n8n_workflows.json)

**6 готовых workflow для автоматизации**

### Workflow 1: Обработка новых лидов
- Автоматически создает клиента в CRM
- Отправляет приветственное сообщение
- Запускается через webhook

### Workflow 2: Автоматический подбор объектов
- Получает предпочтения клиента
- Ищет подходящие объекты
- Отправляет подборку в WhatsApp
- Обновляет данные в CRM

### Workflow 3: Публикация контента по расписанию
- Проверяет расписание каждые 12 часов
- Фильтрует контент на сегодня
- Публикует в Instagram/Facebook
- Обновляет статус

### Workflow 4: Обработка входящих WhatsApp
- Получает сообщения от клиентов
- Обрабатывает через AI-ассистента
- Отправляет умные ответы
- Логирует разговор

### Workflow 5: Генерация контент-пакета
- Запускается в начале месяца
- Создает 10 постов + 15 сторис
- Формирует расписание
- Уведомляет команду

### Workflow 6: Уведомления о горячих лидах
- Отслеживает активность клиентов
- Определяет "горячих" лидов
- Уведомляет менеджера в Telegram
- Передает контактные данные

**Импорт:** Откройте n8n → Import → Загрузите `n8n_workflows.json`

---

## 🗄️ 7. База данных (SQLite)

**Автоматическая CRM система**

### Таблицы:

**clients** - Клиенты
- id, name, phone, channel
- preferences (JSON)
- status, created_at

**properties** - Объекты недвижимости
- id, title, type, price, location
- area, rooms, description
- images (JSON), status

**content** - Контент для публикаций
- id, type (post/story), title, content
- properties (JSON), scheduled_date, status

**База:** `data/crm.db` (создается автоматически)

---

## 📡 8. API Server (api_server.py)

**Главный REST API сервер**

### Основные эндпоинты:

**Чат:**
- `POST /api/chat` - Общение с AI

**MCP для n8n:**
- `POST /api/mcp` - Все MCP команды

**Объекты:**
- `GET /api/properties` - Список объектов
- `POST /api/properties` - Добавить объект

**Клиенты:**
- `POST /api/clients` - Создать клиента
- `GET /api/clients/:id` - Данные клиента

**Контент:**
- `POST /api/content/generate` - Генерация
- `POST /api/content/pack` - Пакет на месяц
- `GET /api/content/schedule` - Расписание

**N8N Webhooks:**
- `POST /n8n/webhook/new_lead` - Новый лид
- `POST /n8n/webhook/property_update` - Обновление объекта
- `POST /n8n/webhook/content_publish` - Публикация

**Виджет:**
- `GET /widget` - Веб-виджет

---

## 🚀 Быстрый старт

### 1. Автоматический запуск:
```bash
./start.sh              # Только API
./start_all.sh          # API + WhatsApp
```

### 2. Ручной запуск:
```bash
python api_server.py           # API на :5000
python whatsapp_bot.py         # WhatsApp на :5001
```

### 3. Тестирование:
```bash
python example_usage.py        # Все примеры
python example_usage.py 1      # Только пример 1
```

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| `README.md` | Полное описание системы |
| `SETUP_GUIDE.md` | Пошаговая установка |
| `MCP_REFERENCE.md` | Справочник по MCP API |
| `n8n_workflows.json` | Готовые workflows |
| `example_usage.py` | Примеры использования |

---

## 🎯 Примеры интеграции с n8n

### Пример 1: Создать клиента
```javascript
// HTTP Request Node в n8n
{
  "method": "POST",
  "url": "http://your-domain.com/api/mcp",
  "body": {
    "action": "create_client",
    "params": {
      "name": "{{$json.name}}",
      "phone": "{{$json.phone}}",
      "channel": "whatsapp"
    }
  }
}
```

### Пример 2: Поиск объектов
```javascript
{
  "method": "POST",
  "url": "http://your-domain.com/api/mcp",
  "body": {
    "action": "search_properties",
    "params": {
      "type": "apartment",
      "max_price": 5000000
    }
  }
}
```

### Пример 3: Отправить в WhatsApp
```javascript
// WhatsApp Node
{
  "to": "{{$json.phone}}",
  "message": "Здравствуйте! Нашли для вас подходящие объекты..."
}
```

---

## 🔑 Требуемые API ключи

| Сервис | Переменная | Где получить |
|--------|------------|--------------|
| OpenAI | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| Telegram | `TELEGRAM_BOT_TOKEN` | @BotFather в Telegram |
| Twilio | `TWILIO_ACCOUNT_SID` | https://www.twilio.com/console |
| Twilio | `TWILIO_AUTH_TOKEN` | https://www.twilio.com/console |

Все ключи добавляются в файл `.env`

---

## 📊 Статистика проекта

📁 **Файлов:** 15+  
🎯 **MCP действий:** 7  
🔄 **N8N workflows:** 6  
🎨 **Типов контента:** 5  
📱 **Каналов коммуникации:** 4 (WhatsApp, сайт, Telegram, n8n)  
🗄️ **Таблиц БД:** 3  
🌐 **API эндпоинтов:** 15+  

---

## ✨ Основные преимущества

✅ **Полная автоматизация** - От лида до сделки без ручной работы  
✅ **AI-powered** - GPT-4 для общения и генерации контента  
✅ **Мультиканальность** - WhatsApp, сайт, Telegram в одной системе  
✅ **Готовые workflows** - 6 проверенных сценариев для n8n  
✅ **Контент-маркетинг** - Автоматическая генерация постов на месяц  
✅ **CRM встроен** - Своя база клиентов и объектов  
✅ **Легкая интеграция** - REST API, webhooks, MCP protocol  
✅ **Open Source** - Весь код доступен и настраиваемый  

---

## 🎉 Готово к использованию!

Все инструменты MCP n8n уже настроены и готовы к работе.

**Следующие шаги:**
1. ✅ Добавьте API ключи в `.env`
2. ✅ Запустите систему: `./start.sh`
3. ✅ Добавьте объекты недвижимости
4. ✅ Импортируйте workflows в n8n
5. ✅ Начните принимать клиентов!

**Полная документация:**
- 📖 README.md
- 🚀 SETUP_GUIDE.md
- 📡 MCP_REFERENCE.md

---

**Вопросы?** Проверьте примеры в `example_usage.py` или документацию!
