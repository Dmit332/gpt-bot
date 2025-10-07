# 🚀 Быстрый старт - AI Real Estate Bot

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка API ключей

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Получите OpenAI API ключ:
   - Перейдите на https://platform.openai.com/api-keys
   - Создайте новый API ключ
   - Вставьте в `.env` файл

3. (Опционально) Настройте Twilio для WhatsApp:
   - Регистрация: https://www.twilio.com/try-twilio
   - Получите Account SID и Auth Token
   - Активируйте WhatsApp Sandbox
   - Вставьте credentials в `.env`

## Шаг 3: Запуск системы

### Вариант А: Быстрый старт (только API)

```bash
python api_server.py
```

Откройте в браузере: http://localhost:5000

### Вариант Б: С WhatsApp ботом

Терминал 1:
```bash
python api_server.py
```

Терминал 2:
```bash
python whatsapp_bot.py
```

## Шаг 4: Тестирование

Запустите примеры использования:

```bash
# Все примеры сразу
python example_usage.py

# Или по отдельности
python example_usage.py 1  # Добавить объекты
python example_usage.py 2  # Поиск объектов
python example_usage.py 3  # Диалог с AI
python example_usage.py 5  # Генерация контента
```

## Шаг 5: Интеграция веб-виджета

Откройте `web_widget.html` в браузере или интегрируйте на сайт:

```html
<!-- Скопируйте содержимое web_widget.html на вашу страницу -->
<!-- ИЛИ подключите как отдельный скрипт -->

<script>
  // В файле web_widget.html измените:
  const API_URL = 'https://your-domain.com'; // На ваш домен
</script>
```

## Шаг 6: Настройка n8n (опционально)

1. Установите n8n:
```bash
npm install n8n -g
n8n start
```

2. Откройте http://localhost:5678

3. Импортируйте workflows из `n8n_workflows.json`

4. В каждом HTTP Request ноде измените URL:
   - `http://localhost:5000` → `https://your-domain.com`

5. Добавьте credentials для:
   - WhatsApp (Twilio)
   - Telegram
   - Instagram (если нужна автопубликация)

## Проверка работоспособности

### 1. API сервер работает?
```bash
curl http://localhost:5000
```
Должен вернуть: `{"status": "online", ...}`

### 2. Добавить тестовый объект:
```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовая квартира",
    "type": "apartment",
    "price": 5000000,
    "location": "Москва",
    "area": 60,
    "rooms": 2,
    "description": "Тестовое описание"
  }'
```

### 3. Поиск объектов:
```bash
curl http://localhost:5000/api/properties
```

### 4. Чат с AI:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test_001",
    "message": "Ищу квартиру в центре",
    "channel": "test"
  }'
```

## Следующие шаги

1. ✅ Добавьте реальные объекты через API или веб-интерфейс
2. ✅ Настройте WhatsApp webhook (если нужен WhatsApp бот)
3. ✅ Интегрируйте веб-виджет на ваш сайт
4. ✅ Настройте n8n workflows для автоматизации
5. ✅ Сгенерируйте контент-пакет на месяц
6. ✅ Начните принимать заявки от клиентов!

## Troubleshooting

### Ошибка: "OpenAI API key not found"
- Убедитесь что файл `.env` создан и содержит `OPENAI_API_KEY`
- Проверьте что ключ валиден на https://platform.openai.com

### Ошибка: "ModuleNotFoundError"
- Установите зависимости: `pip install -r requirements.txt`

### WhatsApp бот не отвечает
- Проверьте Twilio credentials в `.env`
- Убедитесь что webhook настроен в Twilio Console
- Проверьте что `whatsapp_bot.py` запущен

### База данных не создается
- Убедитесь что папка `data/` существует
- Проверьте права на запись

## Полезные команды

```bash
# Просмотр логов
tail -f api_server.log

# Проверка процессов
ps aux | grep python

# Остановка серверов
pkill -f api_server.py
pkill -f whatsapp_bot.py

# Очистка базы данных (будьте осторожны!)
rm data/crm.db
```

## Поддержка

Если что-то не работает:

1. Проверьте все переменные окружения в `.env`
2. Убедитесь что все зависимости установлены
3. Проверьте логи в консоли
4. Запустите `example_usage.py` для проверки функционала

---

**Готово! Система запущена и готова к работе! 🎉**
