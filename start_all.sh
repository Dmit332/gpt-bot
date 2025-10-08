#!/bin/bash

# Запуск всех компонентов системы (API + WhatsApp)
# Использует tmux для управления несколькими сессиями

echo "🏠 AI Real Estate Bot - Полный запуск"
echo "======================================"
echo ""

# Проверка tmux
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux не найден. Устанавливаю..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y tmux
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install tmux
    else
        echo "❌ Установите tmux вручную"
        exit 1
    fi
fi

# Создание папки для данных
mkdir -p data

# Установка зависимостей
echo "📦 Проверка зависимостей..."
pip3 install -r requirements.txt -q

echo ""
echo "🚀 Запуск компонентов в tmux..."
echo ""

# Создаем новую tmux сессию
SESSION="realestate_bot"

# Убиваем предыдущую сессию если существует
tmux kill-session -t $SESSION 2>/dev/null

# Создаем новую сессию
tmux new-session -d -s $SESSION -n "API"

# Окно 1: API Server
tmux send-keys -t $SESSION:0 "python3 api_server.py" C-m

# Окно 2: WhatsApp Bot
tmux new-window -t $SESSION:1 -n "WhatsApp"
tmux send-keys -t $SESSION:1 "sleep 2 && python3 whatsapp_bot.py" C-m

# Окно 3: Команды
tmux new-window -t $SESSION:2 -n "Commands"
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '🎯 Полезные команды:'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '  Примеры: python3 example_usage.py'" C-m
tmux send-keys -t $SESSION:2 "echo '  Тест API: curl http://localhost:5000'" C-m
tmux send-keys -t $SESSION:2 "echo '  Виджет: open http://localhost:5000/widget'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '📊 Мониторинг:'" C-m
tmux send-keys -t $SESSION:2 "echo '  API Server: tmux select-window -t API'" C-m
tmux send-keys -t $SESSION:2 "echo '  WhatsApp Bot: tmux select-window -t WhatsApp'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '❌ Остановка: tmux kill-session -t realestate_bot'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m

# Подключаемся к сессии
echo "✅ Компоненты запущены в tmux!"
echo ""
echo "📊 Доступ к компонентам:"
echo "   - Переключение окон: Ctrl+B затем 0, 1 или 2"
echo "   - Отключение от tmux: Ctrl+B затем D"
echo "   - Остановка всего: tmux kill-session -t $SESSION"
echo ""
echo "🌐 Сервисы:"
echo "   - API: http://localhost:5000"
echo "   - Виджет: http://localhost:5000/widget"
echo "   - WhatsApp: http://localhost:5001/whatsapp/webhook"
echo ""
echo "Подключение к tmux сессии через 3 секунды..."
sleep 3

tmux attach-session -t $SESSION
