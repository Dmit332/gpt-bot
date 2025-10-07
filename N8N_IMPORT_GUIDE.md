# 📥 Инструкция по импорту workflows в n8n

## 🎯 Готовые JSON файлы для импорта

Я создал 6 готовых workflows, которые можно импортировать в n8n одним кликом:

1. **n8n_workflow_1_new_lead.json** - Обработка новых лидов
2. **n8n_workflow_2_property_search.json** - Автоподбор объектов
3. **n8n_workflow_3_content_schedule.json** - Публикация контента
4. **n8n_workflow_4_whatsapp_ai.json** - WhatsApp AI бот
5. **n8n_workflow_5_content_pack.json** - Генерация контент-пакета
6. **n8n_workflow_6_hot_leads.json** - Уведомления о горячих лидах

---

## 📋 Пошаговая инструкция

### Шаг 1: Запустите n8n

```bash
# Если n8n не установлен
npm install n8n -g

# Запуск n8n
n8n start
```

Откройте в браузере: **http://localhost:5678**

---

### Шаг 2: Импорт workflow

**Для каждого файла повторите:**

1. В n8n нажмите **"+"** (новый workflow)
2. Нажмите **"..." (три точки)** в правом верхнем углу
3. Выберите **"Import from File"**
4. Выберите файл (например, `n8n_workflow_1_new_lead.json`)
5. Workflow загрузится автоматически
6. Нажмите **"Save"** для сохранения

**ИЛИ:**

1. Откройте файл в текстовом редакторе
2. Скопируйте весь JSON
3. В n8n: **"..." → "Import from URL"**
4. Вставьте JSON в поле
5. Нажмите **"Import"**

---

### Шаг 3: Настройка URL

**В каждом HTTP Request ноде измените URL:**

Замените `http://localhost:5000` на ваш домен:
- Локально: `http://localhost:5000`
- На сервере: `https://your-domain.com`

**Где изменить:**
- Откройте каждый HTTP Request нод
- Поле **"URL"**
- Замените на ваш URL
- Сохраните

---

### Шаг 4: Настройка переменных окружения (Environment Variables)

В n8n добавьте переменные:

1. Перейдите: **Settings → Variables**
2. Добавьте:

```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_MANAGER_CHAT_ID = your_chat_id
```

**Как получить:**
- **TELEGRAM_BOT_TOKEN**: @BotFather в Telegram
- **TELEGRAM_MANAGER_CHAT_ID**: @userinfobot в Telegram (отправьте /start)

---

### Шаг 5: Активация workflows

Для каждого workflow:

1. Откройте workflow
2. Справа вверху переключатель **"Inactive" → "Active"**
3. Workflow начнет работать!

---

## 🔗 Webhook URLs

После активации получите webhook URLs:

### Workflow 1: Новый лид
```
POST http://localhost:5678/webhook/new-lead
```

**Тестовый запрос:**
```bash
curl -X POST http://localhost:5678/webhook/new-lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "website",
    "preferences": {
      "type": "apartment",
      "max_price": 5000000
    }
  }'
```

### Workflow 2: Поиск объектов
```
POST http://localhost:5678/webhook/search-properties
```

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

### Workflow 4: WhatsApp входящие
```
POST http://localhost:5678/webhook/whatsapp-incoming
```

**Настройка в Twilio:**
1. Twilio Console → WhatsApp → Sandbox Settings
2. "When a message comes in": `http://your-n8n-domain:5678/webhook/whatsapp-incoming`

### Workflow 6: Горячие лиды
```
POST http://localhost:5678/webhook/hot-lead
```

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

## 🧪 Тестирование workflows

### Способ 1: Execute Workflow

1. Откройте workflow в n8n
2. Нажмите **"Execute Workflow"** внизу
3. Для webhook nodes - используйте **"Listen for Test Event"**
4. Отправьте тестовый запрос через curl

### Способ 2: Manual Test Data

1. Кликните на первый нод
2. Нажмите **"Execute Node"**
3. Введите тестовые данные
4. Нажмите **"Execute"**

---

## ⚙️ Расписания

### Workflow 3: Публикация контента
- **Расписание:** Каждые 12 часов
- **Изменить:** Откройте нод "Расписание каждые 12ч"
- **Формат cron:** `0 */12 * * *`

### Workflow 5: Контент-пакет
- **Расписание:** 1-го числа каждого месяца в 9:00
- **Cron:** `0 9 1 * *`
- **Изменить:** Откройте нод "1-го числа в 9:00"

---

## 🔧 Troubleshooting

### Ошибка: "Connection refused"

**Проблема:** n8n не может подключиться к API серверу

**Решение:**
1. Убедитесь что `api_server.py` запущен
2. Проверьте URL в HTTP Request нодах
3. Если n8n в Docker - используйте `host.docker.internal:5000` вместо `localhost:5000`

### Ошибка: "Webhook not found"

**Проблема:** Webhook не активирован

**Решение:**
1. Активируйте workflow (переключатель Active)
2. Подождите 2-3 секунды
3. Webhook URL появится в консоли n8n

### Ошибка в Telegram Node

**Проблема:** Не указаны переменные окружения

**Решение:**
1. Settings → Variables
2. Добавьте `TELEGRAM_BOT_TOKEN` и `TELEGRAM_MANAGER_CHAT_ID`
3. Сохраните и перезапустите workflow

### WhatsApp не отвечает

**Проблема:** Webhook не настроен в Twilio

**Решение:**
1. Twilio Console → WhatsApp → Sandbox
2. Укажите webhook URL от n8n
3. Убедитесь что workflow 4 активен

---

## 📊 Мониторинг

### Просмотр выполнений

1. В n8n перейдите: **"Executions"** (слева)
2. Выберите workflow
3. Посмотрите историю выполнений
4. Кликните на выполнение для деталей

### Логирование

В workflows добавлены ноды "Логирование" которые выводят информацию:
- Откройте выполнение
- Кликните на нод "Логирование"
- Посмотрите данные

---

## 🚀 Production Setup

### Для продакшена:

1. **Используйте HTTPS** для webhook URLs
2. **Настройте аутентификацию** в n8n
3. **Добавьте error handling** в workflows
4. **Настройте retry логику** для HTTP запросов
5. **Включите execution logging** в n8n settings

### Docker Compose пример:

```yaml
version: '3.7'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
      - WEBHOOK_URL=https://your-domain.com/
    volumes:
      - n8n_data:/home/node/.n8n
```

---

## 📝 Чек-лист импорта

- [ ] n8n установлен и запущен
- [ ] API сервер (`api_server.py`) работает
- [ ] Все 6 workflows импортированы
- [ ] URL изменены на ваш домен
- [ ] Переменные окружения добавлены
- [ ] Все workflows активированы
- [ ] Webhook URLs протестированы
- [ ] Telegram уведомления работают
- [ ] WhatsApp webhook настроен в Twilio

---

## 🎉 Готово!

После выполнения всех шагов:

✅ Workflows активированы  
✅ Webhooks работают  
✅ Автоматизация запущена  
✅ Система готова обрабатывать лиды!

**Следующие шаги:**
1. Добавьте объекты недвижимости через API
2. Отправьте тестовый лид через webhook
3. Проверьте генерацию контента
4. Настройте мониторинг

---

**Вопросы?** Проверьте документацию:
- n8n docs: https://docs.n8n.io
- Наш README.md
- MCP_REFERENCE.md
