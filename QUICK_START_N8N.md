# 🚀 Простая инструкция - Импорт в n8n за 5 минут

## Шаг 1: Установите и запустите n8n (если еще не установлен)

### Вариант A: Через NPM (рекомендуется)
```bash
# Установка
npm install n8n -g

# Запуск
n8n start
```

### Вариант B: Через Docker
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Откройте n8n в браузере:
```
http://localhost:5678
```

При первом запуске создайте аккаунт (email + пароль)

---

## Шаг 2: Импорт первого workflow

### Вариант 1 - Через файл (ПРОЩЕ):

1. **В n8n нажмите "+" (плюс)** в верхнем левом углу
   
2. **Нажмите "..." (три точки)** в правом верхнем углу
   
3. **Выберите "Import from File"**
   
4. **Найдите и откройте файл:**
   ```
   n8n_workflow_1_new_lead.json
   ```
   
5. **Workflow загрузится автоматически**
   
6. **Нажмите "Save"** (кнопка справа вверху)

7. **Повторите для всех 6 файлов:**
   - n8n_workflow_1_new_lead.json
   - n8n_workflow_2_property_search.json
   - n8n_workflow_3_content_schedule.json
   - n8n_workflow_4_whatsapp_ai.json
   - n8n_workflow_5_content_pack.json
   - n8n_workflow_6_hot_leads.json

### Вариант 2 - Через копирование (БЫСТРЕЕ):

1. **Откройте файл** в текстовом редакторе (например, `n8n_workflow_1_new_lead.json`)

2. **Выделите весь текст:** `Ctrl+A` (или `Cmd+A` на Mac)

3. **Скопируйте:** `Ctrl+C` (или `Cmd+C`)

4. **В n8n нажмите "+" → "..." → "Import from Clipboard"**

5. **Вставьте:** `Ctrl+V` (или `Cmd+V`)

6. **Нажмите "Import"**

7. **Сохраните** workflow

---

## Шаг 3: Запустите API сервер (наш бэкенд)

В терминале:

```bash
cd /workspace

# Установите зависимости (первый раз)
pip install -r requirements.txt

# Создайте .env файл
cp .env.example .env

# ВАЖНО! Откройте .env и добавьте ваш OPENAI_API_KEY
nano .env  # или любой редактор
```

В файле `.env` добавьте:
```
OPENAI_API_KEY=sk-ваш-ключ-здесь
```

Запустите сервер:
```bash
python api_server.py
```

Сервер запустится на `http://localhost:5000`

---

## Шаг 4: Настройте URL в workflows

**ВАЖНО!** Нужно изменить URL в каждом workflow:

### Если все на одном компьютере:
Оставьте как есть: `http://localhost:5000`

### Если n8n в Docker:
Замените на: `http://host.docker.internal:5000`

### Если на разных серверах:
Замените на: `http://ваш-ip:5000` или `https://ваш-домен.com`

**Как изменить:**

1. Откройте workflow
2. Кликните на нод "HTTP Request" (например, "Создать клиента")
3. Найдите поле **"URL"**
4. Измените `http://localhost:5000` на ваш URL
5. Сохраните
6. Повторите для всех HTTP Request нодов во всех workflows

---

## Шаг 5: Добавьте переменные окружения (для Telegram)

**Только если хотите Telegram уведомления:**

1. В n8n: **Settings (шестеренка слева внизу)**

2. Выберите **"Variables"**

3. Нажмите **"Add Variable"**

4. Добавьте:
   ```
   Имя: TELEGRAM_BOT_TOKEN
   Значение: ваш_токен_от_BotFather
   ```

5. Добавьте еще одну:
   ```
   Имя: TELEGRAM_MANAGER_CHAT_ID
   Значение: ваш_chat_id
   ```

**Как получить токен:**
- Напишите @BotFather в Telegram
- Отправьте `/newbot`
- Следуйте инструкциям
- Скопируйте токен

**Как узнать Chat ID:**
- Напишите @userinfobot в Telegram
- Отправьте `/start`
- Скопируйте ваш ID

---

## Шаг 6: Активируйте workflows

Для каждого workflow:

1. **Откройте workflow**

2. **Справа вверху** найдите переключатель **"Inactive"**

3. **Кликните** чтобы сделать **"Active"**

4. Workflow станет зеленым ✅

5. **Повторите для всех 6 workflows**

---

## Шаг 7: Получите Webhook URLs

После активации у вас появятся webhook URLs:

1. Откройте workflow с webhook (например, Workflow 1)

2. Кликните на первый нод **"Webhook"**

3. В правой панели увидите:
   ```
   Production URL:
   http://localhost:5678/webhook/new-lead
   ```

4. **Скопируйте URL** - он вам понадобится

**Ваши webhook URLs:**
```
1. Новый лид:       http://localhost:5678/webhook/new-lead
2. Поиск объектов:  http://localhost:5678/webhook/search-properties
4. WhatsApp AI:     http://localhost:5678/webhook/whatsapp-incoming
6. Горячие лиды:    http://localhost:5678/webhook/hot-lead
```

---

## Шаг 8: Тестирование

### Проверьте что API сервер работает:

```bash
curl http://localhost:5000
```

Должен вернуть:
```json
{"status": "online", "service": "AI Real Estate Bot", ...}
```

### Добавьте тестовый объект:

```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовая квартира",
    "type": "apartment",
    "price": 5000000,
    "location": "Москва, центр",
    "area": 60,
    "rooms": 2,
    "description": "Отличная квартира для теста"
  }'
```

### Протестируйте Workflow 1 (Новый лид):

```bash
curl -X POST http://localhost:5678/webhook/new-lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест Тестов",
    "phone": "+79991234567",
    "channel": "test"
  }'
```

**Ожидаемый результат:**
```json
{
  "success": true,
  "client_id": "client_...",
  "message": "Клиент создан и приветствие отправлено"
}
```

### Проверьте в n8n:

1. Перейдите в **"Executions"** (слева)
2. Выберите workflow "Новый лид"
3. Увидите выполнение с зеленой галочкой ✅
4. Кликните чтобы посмотреть детали

---

## 🎯 Краткая памятка

**Что нужно для работы:**
1. ✅ n8n запущен (`http://localhost:5678`)
2. ✅ API сервер запущен (`python api_server.py`)
3. ✅ Все 6 workflows импортированы
4. ✅ URL настроены (localhost:5000)
5. ✅ Workflows активированы (Active)
6. ✅ Добавлены тестовые объекты

**Две команды для запуска всего:**

Терминал 1:
```bash
python api_server.py
```

Терминал 2:
```bash
n8n start
```

Браузер:
```
http://localhost:5678
```

---

## 🆘 Частые проблемы

### "Webhook not found"
**Решение:** Активируйте workflow (переключатель Active)

### "Connection refused"
**Решение:** 
1. Проверьте что `api_server.py` запущен
2. Проверьте URL в HTTP Request нодах

### "OpenAI API key not found"
**Решение:**
1. Откройте `.env` файл
2. Добавьте `OPENAI_API_KEY=sk-ваш-ключ`

### Telegram не работает
**Решение:**
1. Settings → Variables
2. Добавьте TELEGRAM_BOT_TOKEN и TELEGRAM_MANAGER_CHAT_ID

### WhatsApp не отвечает
**Решение:**
1. Запустите `python whatsapp_bot.py`
2. Настройте webhook в Twilio Console

---

## 📱 Настройка WhatsApp (опционально)

Если хотите WhatsApp бот:

1. **Зарегистрируйтесь на Twilio:** https://www.twilio.com/try-twilio

2. **Получите WhatsApp Sandbox:**
   - Twilio Console → Messaging → Try it out → WhatsApp
   - Отправьте код на номер Twilio с вашего WhatsApp

3. **Настройте webhook:**
   - В Twilio: Sandbox Settings
   - "When a message comes in": `http://ваш-домен:5678/webhook/whatsapp-incoming`

4. **Запустите WhatsApp бот:**
   ```bash
   python whatsapp_bot.py
   ```

---

## ✅ Чек-лист готовности

Проверьте перед началом работы:

- [ ] n8n установлен и открывается в браузере
- [ ] API сервер запущен (python api_server.py)
- [ ] Все 6 workflows импортированы в n8n
- [ ] URL изменены на localhost:5000 (или ваш)
- [ ] Все workflows активированы (зеленые)
- [ ] OPENAI_API_KEY добавлен в .env
- [ ] Тестовые объекты добавлены в базу
- [ ] Webhook протестирован через curl
- [ ] Видите успешное выполнение в Executions

---

## 🎉 Готово!

Теперь у вас работает:

✅ AI-бот для недвижимости  
✅ Автоматическая обработка лидов  
✅ Подбор объектов  
✅ Генерация контента  
✅ Уведомления менеджерам  
✅ Интеграция с WhatsApp (опционально)  

**Начните работать:**
1. Добавьте реальные объекты через API
2. Отправьте тестовый лид через webhook
3. Проверьте работу в n8n → Executions
4. Интегрируйте на сайт (веб-виджет)

---

**Вопросы?** Смотрите подробные инструкции:
- `N8N_IMPORT_GUIDE.md` - Полная инструкция
- `README.md` - Документация системы
- `example_usage.py` - Примеры на Python

**Успехов! 🚀**
