"""
AI-ассистент для работы с клиентами
Уточняет параметры и подбирает подходящие объекты
"""
import os
import json
from typing import Dict, List, Any
import openai
from mcp_server import mcp_server

openai.api_key = os.environ.get("OPENAI_API_KEY")


class AIAssistant:
    def __init__(self):
        self.conversation_history = {}
        self.system_prompt = """
Ты - профессиональный AI-ассистент по подбору недвижимости. Твоя задача:

1. Приветствовать клиента тепло и дружелюбно
2. Уточнить важные параметры:
   - Тип недвижимости (квартира, дом, коммерческая)
   - Бюджет (минимум и максимум)
   - Локация (район, город)
   - Количество комнат
   - Площадь
   - Дополнительные пожелания
3. На основе параметров подобрать подходящие варианты
4. Презентовать объекты профессионально и убедительно
5. Предложить организовать просмотр

Общайся естественно, задавай уточняющие вопросы по одному-два параметра за раз.
Будь внимательным к пожеланиям клиента и гибко адаптируй свои рекомендации.
"""
    
    def get_conversation(self, client_id: str) -> List[Dict]:
        """Получить историю разговора"""
        if client_id not in self.conversation_history:
            self.conversation_history[client_id] = [
                {"role": "system", "content": self.system_prompt}
            ]
        return self.conversation_history[client_id]
    
    def add_message(self, client_id: str, role: str, content: str):
        """Добавить сообщение в историю"""
        conversation = self.get_conversation(client_id)
        conversation.append({"role": role, "content": content})
    
    def extract_preferences(self, message: str, current_preferences: Dict) -> Dict:
        """Извлечь предпочтения из сообщения клиента"""
        # Используем GPT для извлечения структурированных данных
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """
Извлеки параметры недвижимости из сообщения клиента.
Верни JSON с полями: type, min_price, max_price, location, rooms, area.
Если параметр не указан, не включай его в ответ.
Цены указывай в числовом формате без валюты.
"""},
                    {"role": "user", "content": message}
                ],
                temperature=0.3
            )
            
            extracted = json.loads(response.choices[0].message.content)
            # Обновляем текущие предпочтения
            current_preferences.update(extracted)
            
        except Exception as e:
            print(f"Ошибка извлечения предпочтений: {e}")
        
        return current_preferences
    
    def search_and_format_properties(self, preferences: Dict) -> str:
        """Поиск объектов и форматирование результатов"""
        properties = mcp_server.search_properties(preferences)
        
        if not properties:
            return "К сожалению, по вашим критериям не нашлось подходящих вариантов. Давайте попробуем изменить параметры поиска?"
        
        # Форматируем результаты
        response = f"Отлично! Нашёл для вас {len(properties)} подходящих вариантов:\n\n"
        
        for i, prop in enumerate(properties[:5], 1):  # Показываем топ-5
            response += f"🏠 **Вариант {i}: {prop['title']}**\n"
            response += f"💰 Цена: {prop['price']:,.0f} ₽\n"
            response += f"📍 Локация: {prop['location']}\n"
            response += f"📐 Площадь: {prop['area']} м²\n"
            response += f"🚪 Комнат: {prop['rooms']}\n"
            response += f"📝 {prop['description'][:100]}...\n\n"
        
        response += "Какой вариант вам интересен? Могу рассказать подробнее или организовать просмотр! 😊"
        
        return response
    
    async def process_message(self, client_id: str, message: str, 
                             channel: str = "unknown") -> str:
        """Обработать сообщение от клиента"""
        
        # Получаем или создаём клиента
        client = mcp_server.get_client(client_id)
        if not client:
            # Первое сообщение - создаём клиента
            client = mcp_server.create_client(
                name="Новый клиент",
                phone="",
                channel=channel,
                preferences={}
            )
            client_id = client['id']
        
        # Добавляем сообщение в историю
        self.add_message(client_id, "user", message)
        
        # Извлекаем предпочтения
        preferences = self.extract_preferences(message, client.get('preferences', {}))
        
        # Обновляем предпочтения в базе
        if preferences != client.get('preferences', {}):
            mcp_server.update_client_preferences(client_id, preferences)
        
        # Проверяем, достаточно ли данных для поиска
        has_enough_data = any([
            'type' in preferences,
            'min_price' in preferences or 'max_price' in preferences,
            'location' in preferences,
            'rooms' in preferences
        ])
        
        # Формируем контекст для GPT
        context = f"Текущие предпочтения клиента: {json.dumps(preferences, ensure_ascii=False)}"
        
        if has_enough_data and len(preferences) >= 2:
            # Ищем объекты
            properties_text = self.search_and_format_properties(preferences)
            context += f"\n\nНайденные объекты:\n{properties_text}"
        
        # Получаем ответ от GPT
        conversation = self.get_conversation(client_id)
        conversation.append({"role": "assistant", "content": context})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            self.add_message(client_id, "assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"Извините, произошла ошибка. Попробуйте ещё раз. ({str(e)})"
    
    def generate_welcome_message(self, channel: str) -> str:
        """Генерировать приветственное сообщение"""
        messages = {
            "whatsapp": "Привет! 👋 Я AI-ассистент по подбору недвижимости. Помогу найти идеальный вариант для вас! Расскажите, что ищете?",
            "website": "Здравствуйте! Я помогу подобрать недвижимость под ваши пожелания. Какой объект вас интересует?",
            "telegram": "Привет! 🏠 Ищете недвижимость? Я помогу! Расскажите о ваших предпочтениях."
        }
        return messages.get(channel, messages["website"])


# Инициализация ассистента
ai_assistant = AIAssistant()
