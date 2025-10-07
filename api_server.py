"""
Главный API сервер
Объединяет все компоненты: MCP, AI-ассистент, WhatsApp, веб-виджет
"""
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
from mcp_server import mcp_server, handle_mcp_request
from ai_assistant import ai_assistant
from content_generator import content_generator

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для веб-виджета


# === Основной API ===

@app.route('/')
def index():
    return {
        "status": "online",
        "service": "AI Real Estate Bot",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "mcp": "/api/mcp",
            "properties": "/api/properties",
            "content": "/api/content",
            "widget": "/widget"
        }
    }


# === Чат API ===

@app.route('/api/chat', methods=['POST'])
async def chat():
    """Обработка сообщений от клиентов"""
    try:
        data = request.json
        client_id = data.get('client_id')
        message = data.get('message')
        channel = data.get('channel', 'website')
        
        if not client_id or not message:
            return jsonify({"error": "Missing client_id or message"}), 400
        
        # Обрабатываем через AI-ассистента
        response = await ai_assistant.process_message(client_id, message, channel)
        
        return jsonify({
            "client_id": client_id,
            "response": response,
            "timestamp": os.times().elapsed
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === MCP API для n8n ===

@app.route('/api/mcp', methods=['POST'])
def mcp_endpoint():
    """MCP эндпоинт для n8n"""
    try:
        data = request.json
        action = data.get('action')
        params = data.get('params', {})
        
        if not action:
            return jsonify({"error": "Missing action"}), 400
        
        result = handle_mcp_request(action, params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === API управления объектами ===

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """Получить список объектов"""
    try:
        filters = {}
        
        # Фильтры из query параметров
        if request.args.get('type'):
            filters['type'] = request.args.get('type')
        if request.args.get('min_price'):
            filters['min_price'] = float(request.args.get('min_price'))
        if request.args.get('max_price'):
            filters['max_price'] = float(request.args.get('max_price'))
        if request.args.get('location'):
            filters['location'] = request.args.get('location')
        if request.args.get('rooms'):
            filters['rooms'] = int(request.args.get('rooms'))
        
        properties = mcp_server.search_properties(filters)
        return jsonify({"properties": properties, "count": len(properties)})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/properties', methods=['POST'])
def add_property():
    """Добавить новый объект"""
    try:
        data = request.json
        
        property_obj = mcp_server.add_property(
            title=data['title'],
            type=data['type'],
            price=data['price'],
            location=data['location'],
            area=data['area'],
            rooms=data['rooms'],
            description=data['description'],
            images=data.get('images', [])
        )
        
        return jsonify(property_obj), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === API управления клиентами ===

@app.route('/api/clients', methods=['POST'])
def create_client():
    """Создать клиента"""
    try:
        data = request.json
        client = mcp_server.create_client(
            name=data['name'],
            phone=data.get('phone', ''),
            channel=data.get('channel', 'website'),
            preferences=data.get('preferences', {})
        )
        return jsonify(client), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    """Получить данные клиента"""
    try:
        client = mcp_server.get_client(client_id)
        if client:
            return jsonify(client)
        return jsonify({"error": "Client not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === API генерации контента ===

@app.route('/api/content/generate', methods=['POST'])
def generate_content():
    """Генерировать контент"""
    try:
        data = request.json
        content_type = data.get('type', 'post')
        template = data.get('template', 'property_showcase')
        properties = data.get('properties', [])
        topic = data.get('topic')
        
        if content_type == 'story' and properties:
            # Генерируем сторис
            text = content_generator.generate_story_text(properties[0])
        else:
            # Генерируем пост
            text = content_generator.generate_post_text(template, properties, topic)
        
        return jsonify({
            "type": content_type,
            "text": text,
            "generated_at": os.times().elapsed
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/content/pack', methods=['POST'])
def create_content_pack():
    """Создать контент-пакет на месяц"""
    try:
        data = request.json
        num_posts = data.get('posts', 10)
        num_stories = data.get('stories', 15)
        
        pack = content_generator.create_content_pack(num_posts, num_stories)
        
        return jsonify(pack)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/content/schedule', methods=['GET'])
def get_content_schedule():
    """Получить расписание контента"""
    try:
        limit = int(request.args.get('limit', 30))
        schedule = mcp_server.get_content_schedule(limit)
        return jsonify({"schedule": schedule, "count": len(schedule)})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Веб-виджет ===

@app.route('/widget')
def widget():
    """Отдать веб-виджет"""
    return send_file('web_widget.html')


# === n8n Webhooks ===

@app.route('/n8n/webhook/<workflow_name>', methods=['POST'])
def n8n_webhook(workflow_name):
    """Общий webhook для n8n"""
    try:
        data = request.json
        
        # Обрабатываем разные типы workflow
        if workflow_name == 'new_lead':
            # Создаем нового клиента
            client = mcp_server.create_client(
                name=data.get('name', 'Новый лид'),
                phone=data.get('phone', ''),
                channel=data.get('channel', 'n8n'),
                preferences=data.get('preferences', {})
            )
            return jsonify({"status": "created", "client": client})
        
        elif workflow_name == 'property_update':
            # Добавляем/обновляем объект
            property_obj = mcp_server.add_property(**data)
            return jsonify({"status": "created", "property": property_obj})
        
        elif workflow_name == 'content_publish':
            # Публикуем контент
            return jsonify({"status": "published", "data": data})
        
        else:
            return jsonify({"error": f"Unknown workflow: {workflow_name}"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 AI Real Estate Bot Server запущен")
    print("📍 API доступен на: http://localhost:5000")
    print("💬 Веб-виджет: http://localhost:5000/widget")
    print("🔗 MCP эндпоинт: http://localhost:5000/api/mcp")
    print("\nДоступные эндпоинты:")
    print("  - POST /api/chat - Чат с AI-ассистентом")
    print("  - POST /api/mcp - MCP команды для n8n")
    print("  - GET/POST /api/properties - Управление объектами")
    print("  - POST /api/content/generate - Генерация контента")
    print("  - POST /api/content/pack - Создание контент-пакета")
    print("  - POST /n8n/webhook/<workflow> - Webhooks для n8n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
