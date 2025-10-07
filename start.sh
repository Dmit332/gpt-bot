#!/bin/bash

# AI Real Estate Bot - Скрипт быстрого старта
# Автоматически устанавливает зависимости и запускает систему

echo "🏠 AI Real Estate Bot - Быстрый старт"
echo "======================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8+"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip не найден. Установите pip"
    exit 1
fi

echo "✅ pip найден"
echo ""

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Ошибка установки зависимостей"
    exit 1
fi

echo ""
echo "✅ Зависимости установлены"
echo ""

# Проверка .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден"
    echo "📝 Создаю из .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваш OPENAI_API_KEY"
    echo "   Получить ключ: https://platform.openai.com/api-keys"
    echo ""
    read -p "Нажмите Enter когда добавите API ключ в .env..."
fi

# Создание папки для данных
mkdir -p data

echo ""
echo "🚀 Запуск API сервера..."
echo "   API: http://localhost:5000"
echo "   Виджет: http://localhost:5000/widget"
echo ""
echo "   Остановка: Ctrl+C"
echo ""

# Запуск сервера
python3 api_server.py
