"""
MCP Server для интеграции с n8n
Предоставляет инструменты для управления клиентами, объектами и контентом
"""
import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import sqlite3


@dataclass
class Client:
    id: str
    name: str
    phone: str
    channel: str  # whatsapp, website, telegram
    preferences: Dict[str, Any]
    status: str  # new, in_progress, qualified, closed
    created_at: str


@dataclass
class Property:
    id: str
    title: str
    type: str  # apartment, house, commercial
    price: float
    location: str
    area: float
    rooms: int
    description: str
    images: List[str]
    status: str  # available, reserved, sold


@dataclass
class ContentPost:
    id: str
    type: str  # post, story
    title: str
    content: str
    properties: List[str]  # property IDs
    scheduled_date: str
    status: str  # draft, scheduled, published


class MCPServer:
    def __init__(self, db_path="data/crm.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица клиентов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                channel TEXT,
                preferences TEXT,
                status TEXT,
                created_at TEXT
            )
        ''')
        
        # Таблица объектов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id TEXT PRIMARY KEY,
                title TEXT,
                type TEXT,
                price REAL,
                location TEXT,
                area REAL,
                rooms INTEGER,
                description TEXT,
                images TEXT,
                status TEXT
            )
        ''')
        
        # Таблица контента
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id TEXT PRIMARY KEY,
                type TEXT,
                title TEXT,
                content TEXT,
                properties TEXT,
                scheduled_date TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # === Управление клиентами ===
    
    def create_client(self, name: str, phone: str, channel: str, preferences: Dict = None) -> Dict:
        """Создать нового клиента"""
        client = Client(
            id=f"client_{datetime.now().timestamp()}",
            name=name,
            phone=phone,
            channel=channel,
            preferences=preferences or {},
            status="new",
            created_at=datetime.now().isoformat()
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (client.id, client.name, client.phone, client.channel, 
              json.dumps(client.preferences), client.status, client.created_at))
        conn.commit()
        conn.close()
        
        return asdict(client)
    
    def update_client_preferences(self, client_id: str, preferences: Dict) -> Dict:
        """Обновить предпочтения клиента"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clients SET preferences = ?, status = 'in_progress'
            WHERE id = ?
        ''', (json.dumps(preferences), client_id))
        conn.commit()
        conn.close()
        
        return {"status": "updated", "client_id": client_id}
    
    def get_client(self, client_id: str) -> Dict:
        """Получить данные клиента"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0], "name": row[1], "phone": row[2],
                "channel": row[3], "preferences": json.loads(row[4]),
                "status": row[5], "created_at": row[6]
            }
        return None
    
    # === Управление объектами ===
    
    def add_property(self, title: str, type: str, price: float, location: str,
                     area: float, rooms: int, description: str, images: List[str] = None) -> Dict:
        """Добавить объект недвижимости"""
        property_obj = Property(
            id=f"prop_{datetime.now().timestamp()}",
            title=title,
            type=type,
            price=price,
            location=location,
            area=area,
            rooms=rooms,
            description=description,
            images=images or [],
            status="available"
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO properties VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (property_obj.id, property_obj.title, property_obj.type, property_obj.price,
              property_obj.location, property_obj.area, property_obj.rooms,
              property_obj.description, json.dumps(property_obj.images), property_obj.status))
        conn.commit()
        conn.close()
        
        return asdict(property_obj)
    
    def search_properties(self, filters: Dict) -> List[Dict]:
        """Поиск объектов по фильтрам"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM properties WHERE status = "available"'
        params = []
        
        if 'type' in filters:
            query += ' AND type = ?'
            params.append(filters['type'])
        
        if 'min_price' in filters:
            query += ' AND price >= ?'
            params.append(filters['min_price'])
        
        if 'max_price' in filters:
            query += ' AND price <= ?'
            params.append(filters['max_price'])
        
        if 'rooms' in filters:
            query += ' AND rooms = ?'
            params.append(filters['rooms'])
        
        if 'location' in filters:
            query += ' AND location LIKE ?'
            params.append(f"%{filters['location']}%")
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        properties = []
        for row in rows:
            properties.append({
                "id": row[0], "title": row[1], "type": row[2],
                "price": row[3], "location": row[4], "area": row[5],
                "rooms": row[6], "description": row[7],
                "images": json.loads(row[8]), "status": row[9]
            })
        
        return properties
    
    # === Управление контентом ===
    
    def create_content(self, type: str, title: str, content: str,
                      properties: List[str] = None, scheduled_date: str = None) -> Dict:
        """Создать контент (пост/сторис)"""
        content_obj = ContentPost(
            id=f"content_{datetime.now().timestamp()}",
            type=type,
            title=title,
            content=content,
            properties=properties or [],
            scheduled_date=scheduled_date or datetime.now().isoformat(),
            status="draft"
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO content VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (content_obj.id, content_obj.type, content_obj.title, content_obj.content,
              json.dumps(content_obj.properties), content_obj.scheduled_date, content_obj.status))
        conn.commit()
        conn.close()
        
        return asdict(content_obj)
    
    def get_content_schedule(self, limit: int = 10) -> List[Dict]:
        """Получить расписание контента"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM content ORDER BY scheduled_date DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        content_list = []
        for row in rows:
            content_list.append({
                "id": row[0], "type": row[1], "title": row[2],
                "content": row[3], "properties": json.loads(row[4]),
                "scheduled_date": row[5], "status": row[6]
            })
        
        return content_list
    
    # === N8N Webhook методы ===
    
    def trigger_n8n_workflow(self, workflow_id: str, data: Dict) -> Dict:
        """Триггер для n8n workflow"""
        return {
            "workflow_id": workflow_id,
            "triggered_at": datetime.now().isoformat(),
            "data": data,
            "status": "triggered"
        }


# Инициализация сервера
mcp_server = MCPServer()


# === API для n8n ===

def handle_mcp_request(action: str, params: Dict) -> Dict:
    """Обработчик запросов от n8n"""
    
    if action == "create_client":
        return mcp_server.create_client(**params)
    
    elif action == "update_preferences":
        return mcp_server.update_client_preferences(**params)
    
    elif action == "get_client":
        return mcp_server.get_client(**params)
    
    elif action == "add_property":
        return mcp_server.add_property(**params)
    
    elif action == "search_properties":
        return mcp_server.search_properties(params)
    
    elif action == "create_content":
        return mcp_server.create_content(**params)
    
    elif action == "get_content_schedule":
        return mcp_server.get_content_schedule(params.get("limit", 10))
    
    else:
        return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    print("MCP Server инициализирован")
    print("Доступные действия:")
    print("  - create_client: Создать клиента")
    print("  - update_preferences: Обновить предпочтения клиента")
    print("  - add_property: Добавить объект")
    print("  - search_properties: Поиск объектов")
    print("  - create_content: Создать контент")
    print("  - get_content_schedule: Получить расписание контента")
