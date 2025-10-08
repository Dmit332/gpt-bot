# 📡 MCP Server - Справочник по API

Model Context Protocol (MCP) сервер для интеграции с n8n и автоматизации процессов.

## 🔗 Базовый URL

```
http://your-domain.com/api/mcp
```

## 📋 Формат запроса

Все запросы отправляются методом POST с JSON телом:

```json
{
  "action": "название_действия",
  "params": {
    "параметр1": "значение1",
    "параметр2": "значение2"
  }
}
```

---

## 🎯 Доступные действия (Actions)

### 1. create_client
**Создать нового клиента в CRM**

**Параметры:**
```json
{
  "action": "create_client",
  "params": {
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "whatsapp",  // website, telegram, whatsapp, n8n
    "preferences": {
      "type": "apartment",
      "min_price": 3000000,
      "max_price": 5000000
    }
  }
}
```

**Ответ:**
```json
{
  "id": "client_1234567890.123",
  "name": "Иван Петров",
  "phone": "+79991234567",
  "channel": "whatsapp",
  "preferences": {...},
  "status": "new",
  "created_at": "2025-10-07T10:30:00"
}
```

---

### 2. update_preferences
**Обновить предпочтения клиента**

**Параметры:**
```json
{
  "action": "update_preferences",
  "params": {
    "client_id": "client_1234567890.123",
    "preferences": {
      "type": "apartment",
      "min_price": 4000000,
      "max_price": 6000000,
      "rooms": 3,
      "location": "Москва, центр"
    }
  }
}
```

**Ответ:**
```json
{
  "status": "updated",
  "client_id": "client_1234567890.123"
}
```

---

### 3. get_client
**Получить данные клиента**

**Параметры:**
```json
{
  "action": "get_client",
  "params": {
    "client_id": "client_1234567890.123"
  }
}
```

**Ответ:**
```json
{
  "id": "client_1234567890.123",
  "name": "Иван Петров",
  "phone": "+79991234567",
  "channel": "whatsapp",
  "preferences": {...},
  "status": "in_progress",
  "created_at": "2025-10-07T10:30:00"
}
```

---

### 4. add_property
**Добавить объект недвижимости**

**Параметры:**
```json
{
  "action": "add_property",
  "params": {
    "title": "2-комнатная квартира в центре",
    "type": "apartment",  // apartment, house, commercial
    "price": 4500000,
    "location": "Москва, Центральный район",
    "area": 65,
    "rooms": 2,
    "description": "Описание объекта...",
    "images": ["url1.jpg", "url2.jpg"]
  }
}
```

**Ответ:**
```json
{
  "id": "prop_1234567890.123",
  "title": "2-комнатная квартира в центре",
  "type": "apartment",
  "price": 4500000,
  "location": "Москва, Центральный район",
  "area": 65,
  "rooms": 2,
  "description": "...",
  "images": [...],
  "status": "available"
}
```

---

### 5. search_properties
**Поиск объектов по фильтрам**

**Параметры:**
```json
{
  "action": "search_properties",
  "params": {
    "type": "apartment",
    "min_price": 3000000,
    "max_price": 5000000,
    "rooms": 2,
    "location": "Москва"
  }
}
```

Все параметры опциональны. Возможные фильтры:
- `type`: apartment, house, commercial
- `min_price`: минимальная цена
- `max_price`: максимальная цена
- `rooms`: количество комнат
- `location`: локация (поиск по подстроке)

**Ответ:**
```json
[
  {
    "id": "prop_123",
    "title": "...",
    "type": "apartment",
    "price": 4500000,
    "location": "Москва",
    "area": 65,
    "rooms": 2,
    "description": "...",
    "images": [...],
    "status": "available"
  },
  ...
]
```

---

### 6. create_content
**Создать контент (пост/сторис)**

**Параметры:**
```json
{
  "action": "create_content",
  "params": {
    "type": "post",  // post или story
    "title": "Название контента",
    "content": "Текст поста/сторис...",
    "properties": ["prop_123", "prop_456"],  // ID объектов
    "scheduled_date": "2025-10-15T10:00:00"
  }
}
```

**Ответ:**
```json
{
  "id": "content_1234567890.123",
  "type": "post",
  "title": "Название контента",
  "content": "Текст...",
  "properties": [...],
  "scheduled_date": "2025-10-15T10:00:00",
  "status": "draft"
}
```

---

### 7. get_content_schedule
**Получить расписание контента**

**Параметры:**
```json
{
  "action": "get_content_schedule",
  "params": {
    "limit": 30
  }
}
```

**Ответ:**
```json
[
  {
    "id": "content_123",
    "type": "post",
    "title": "...",
    "content": "...",
    "properties": [...],
    "scheduled_date": "2025-10-15T10:00:00",
    "status": "scheduled"
  },
  ...
]
```

---

## 🔌 Примеры использования в n8n

### HTTP Request Node для n8n

**Базовая конфигурация:**
- Method: POST
- URL: `http://your-domain.com/api/mcp`
- Authentication: None (добавьте если нужно)
- Body Content Type: JSON

**Пример 1: Создать клиента**
```json
{
  "action": "create_client",
  "params": {
    "name": "{{ $json.name }}",
    "phone": "{{ $json.phone }}",
    "channel": "whatsapp",
    "preferences": {}
  }
}
```

**Пример 2: Поиск объектов для клиента**
```json
{
  "action": "search_properties",
  "params": {
    "type": "{{ $json.preferences.type }}",
    "min_price": "{{ $json.preferences.min_price }}",
    "max_price": "{{ $json.preferences.max_price }}"
  }
}
```

**Пример 3: Получить контент на сегодня**
```json
{
  "action": "get_content_schedule",
  "params": {
    "limit": 10
  }
}
```

---

## 🌐 Дополнительные REST API эндпоинты

Помимо MCP, доступны прямые REST эндпоинты:

### GET /api/properties
Получить объекты с query параметрами:
```
GET /api/properties?type=apartment&max_price=5000000
```

### POST /api/properties
Добавить объект напрямую (без MCP обертки)

### POST /api/chat
Общение с AI-ассистентом:
```json
{
  "client_id": "client_123",
  "message": "Ищу квартиру в центре",
  "channel": "website"
}
```

### POST /api/content/generate
Генерировать контент через GPT-4:
```json
{
  "type": "post",
  "template": "property_showcase",
  "properties": [...]
}
```

### POST /api/content/pack
Создать контент-пакет на месяц:
```json
{
  "posts": 10,
  "stories": 15
}
```

### GET /api/content/schedule
Получить расписание публикаций:
```
GET /api/content/schedule?limit=30
```

---

## 📊 Статусы и типы данных

### Статусы клиентов:
- `new` - новый лид
- `in_progress` - в работе
- `qualified` - квалифицированный (готов к сделке)
- `closed` - сделка закрыта

### Типы недвижимости:
- `apartment` - квартира
- `house` - дом
- `commercial` - коммерческая недвижимость

### Типы контента:
- `post` - пост для соцсетей
- `story` - сторис

### Статусы контента:
- `draft` - черновик
- `scheduled` - запланирован
- `published` - опубликован

### Каналы коммуникации:
- `website` - веб-сайт
- `whatsapp` - WhatsApp
- `telegram` - Telegram
- `n8n` - через n8n webhook

---

## 🔒 Безопасность

### Для продакшена рекомендуется:

1. **API ключи**: Добавьте аутентификацию через API keys
```python
@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if api_key != os.environ.get('API_KEY'):
        return jsonify({"error": "Invalid API key"}), 401
```

2. **Rate limiting**: Ограничьте количество запросов
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])
```

3. **HTTPS**: Используйте только HTTPS в продакшене

4. **Валидация**: Проверяйте входные данные

---

## 🧪 Тестирование MCP API

### С помощью curl:

```bash
# Создать клиента
curl -X POST http://localhost:5000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create_client",
    "params": {
      "name": "Test Client",
      "phone": "+79999999999",
      "channel": "test"
    }
  }'

# Поиск объектов
curl -X POST http://localhost:5000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "action": "search_properties",
    "params": {
      "type": "apartment",
      "max_price": 5000000
    }
  }'

# Получить расписание
curl -X POST http://localhost:5000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_content_schedule",
    "params": {"limit": 5}
  }'
```

### С помощью Python:

```python
import requests

MCP_URL = "http://localhost:5000/api/mcp"

# Создать клиента
response = requests.post(MCP_URL, json={
    "action": "create_client",
    "params": {
        "name": "Python Test",
        "phone": "+79991234567",
        "channel": "api"
    }
})

print(response.json())
```

---

## 📚 Полная документация

Для полной документации см.:
- `README.md` - Общий обзор системы
- `SETUP_GUIDE.md` - Руководство по установке
- `n8n_workflows.json` - Готовые workflow примеры
- `example_usage.py` - Примеры использования на Python

---

**Готово к использованию! 🚀**
