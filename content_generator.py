"""
Генератор контента для социальных сетей
Создает посты и сторис для Instagram/Facebook с подборками объектов
"""
import os
import openai
from typing import List, Dict
from datetime import datetime, timedelta
from mcp_server import mcp_server

openai.api_key = os.environ.get("OPENAI_API_KEY")


class ContentGenerator:
    def __init__(self):
        self.post_templates = {
            "property_showcase": "Покажи объект недвижимости привлекательно",
            "selection": "Подборка объектов по теме",
            "tips": "Полезные советы по недвижимости",
            "success_story": "История успешной сделки",
            "market_update": "Обзор рынка недвижимости"
        }
    
    def generate_post_text(self, template_type: str, properties: List[Dict] = None,
                          topic: str = None) -> str:
        """Генерировать текст поста с помощью GPT-4"""
        
        if template_type == "property_showcase" and properties:
            prop = properties[0]
            prompt = f"""
Создай привлекательный пост для Instagram о продаже недвижимости.

Объект:
- Название: {prop['title']}
- Тип: {prop['type']}
- Цена: {prop['price']:,.0f} ₽
- Локация: {prop['location']}
- Площадь: {prop['area']} м²
- Комнат: {prop['rooms']}
- Описание: {prop['description']}

Требования:
- Начни с цепляющего заголовка с эмоджи
- Используй эмоджи по тексту
- Подчеркни уникальные преимущества
- Добавь призыв к действию
- Максимум 1500 символов
- Используй хэштеги в конце

Стиль: профессионально, но дружелюбно
"""
        
        elif template_type == "selection" and properties:
            prompt = f"""
Создай пост с подборкой {len(properties)} объектов недвижимости для Instagram.

Тема подборки: {topic or 'Лучшие предложения недели'}

Объекты:
"""
            for i, prop in enumerate(properties, 1):
                prompt += f"\n{i}. {prop['title']} - {prop['price']:,.0f} ₽, {prop['location']}"
            
            prompt += """

Требования:
- Захватывающий заголовок с эмоджи
- Краткое описание каждого объекта (2-3 строки)
- Эмоджи для каждого пункта
- Призыв к действию
- Хэштеги в конце
- Максимум 2000 символов

Стиль: энергичный, мотивирующий
"""
        
        elif template_type == "tips":
            prompt = f"""
Создай полезный пост с советами по недвижимости для Instagram.

Тема: {topic or 'Как выбрать квартиру'}

Требования:
- Цепляющий заголовок
- 5-7 практических советов
- Эмоджи для каждого совета
- Легко читается
- Призыв к действию
- Хэштеги
- Максимум 1800 символов

Стиль: экспертный, но понятный
"""
        
        else:
            prompt = f"Создай пост о недвижимости на тему: {topic}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты - креативный копирайтер, специализирующийся на недвижимости и контенте для соцсетей."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Ошибка генерации контента: {e}")
            return "Ошибка генерации контента"
    
    def generate_story_text(self, property_data: Dict) -> str:
        """Генерировать текст для сторис"""
        prompt = f"""
Создай короткий цепляющий текст для Instagram Stories о недвижимости.

Объект: {property_data['title']}
Цена: {property_data['price']:,.0f} ₽
Локация: {property_data['location']}

Требования:
- Максимум 80 символов
- Используй 2-3 эмоджи
- Создай интригу или срочность
- Без хэштегов

Примеры стиля:
"🔥 Новинка! Квартира с видом на море"
"⚡️ Последний шанс! Цена снижена"
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты создаешь короткие цепляющие тексты для Instagram Stories."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=50
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Ошибка генерации сторис: {e}")
            return "🏠 Новый объект!"
    
    def create_content_pack(self, num_posts: int = 10, num_stories: int = 15) -> Dict:
        """Создать контент-пакет на месяц"""
        
        # Получаем доступные объекты
        all_properties = mcp_server.search_properties({})
        
        if not all_properties:
            return {"error": "Нет объектов для создания контента"}
        
        content_pack = {
            "posts": [],
            "stories": [],
            "schedule": []
        }
        
        # Генерируем посты
        post_types = [
            ("property_showcase", 4),  # 4 поста с объектами
            ("selection", 3),  # 3 подборки
            ("tips", 2),  # 2 с советами
            ("success_story", 1)  # 1 история успеха
        ]
        
        post_count = 0
        start_date = datetime.now()
        
        for post_type, count in post_types:
            for i in range(count):
                if post_count >= num_posts:
                    break
                
                # Выбираем случайные объекты
                if post_type == "property_showcase":
                    properties = [all_properties[post_count % len(all_properties)]]
                    topic = None
                elif post_type == "selection":
                    start_idx = (post_count * 3) % len(all_properties)
                    properties = all_properties[start_idx:start_idx+3]
                    topics = ["Лучшие предложения недели", "Квартиры до 5 млн", "Новостройки с отделкой"]
                    topic = topics[i % len(topics)]
                else:
                    properties = None
                    topics = [
                        "Как выбрать квартиру",
                        "7 ошибок при покупке жилья",
                        "Инвестиции в недвижимость"
                    ]
                    topic = topics[i % len(topics)]
                
                # Генерируем текст
                text = self.generate_post_text(post_type, properties, topic)
                
                # Планируем дату публикации
                scheduled_date = start_date + timedelta(days=post_count * 3)
                
                # Сохраняем в базу
                property_ids = [p['id'] for p in properties] if properties else []
                content = mcp_server.create_content(
                    type="post",
                    title=f"{post_type}_{post_count+1}",
                    content=text,
                    properties=property_ids,
                    scheduled_date=scheduled_date.isoformat()
                )
                
                content_pack["posts"].append(content)
                post_count += 1
        
        # Генерируем сторис
        for i in range(min(num_stories, len(all_properties))):
            property_data = all_properties[i % len(all_properties)]
            story_text = self.generate_story_text(property_data)
            
            scheduled_date = start_date + timedelta(days=i * 2)
            
            content = mcp_server.create_content(
                type="story",
                title=f"story_{i+1}",
                content=story_text,
                properties=[property_data['id']],
                scheduled_date=scheduled_date.isoformat()
            )
            
            content_pack["stories"].append(content)
        
        # Формируем расписание
        all_content = content_pack["posts"] + content_pack["stories"]
        all_content.sort(key=lambda x: x['scheduled_date'])
        
        for item in all_content:
            content_pack["schedule"].append({
                "date": item['scheduled_date'][:10],
                "type": item['type'],
                "title": item['title'],
                "id": item['id']
            })
        
        return content_pack
    
    def generate_review_post(self, client_name: str, review_text: str,
                            property_data: Dict = None) -> str:
        """Генерировать пост с отзывом клиента"""
        prompt = f"""
Создай пост для Instagram с отзывом клиента о покупке недвижимости.

Клиент: {client_name}
Отзыв: "{review_text}"
"""
        
        if property_data:
            prompt += f"\nОбъект: {property_data['title']}, {property_data['location']}"
        
        prompt += """

Требования:
- Благодарность клиенту в начале
- Процитировать отзыв красиво
- Добавить детали успешной сделки
- Эмоджи
- Призыв написать нам
- Хэштеги про отзывы и недвижимость
- Максимум 1500 символов

Стиль: искренний, радостный
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты создаешь посты с отзывами клиентов."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Ошибка генерации поста с отзывом: {e}")
            return f"Отзыв от {client_name}: {review_text}"


# Инициализация генератора
content_generator = ContentGenerator()


if __name__ == "__main__":
    print("Content Generator инициализирован")
    print("Доступные функции:")
    print("  - generate_post_text: Генерация текста поста")
    print("  - generate_story_text: Генерация текста сторис")
    print("  - create_content_pack: Создание контент-пакета на месяц")
    print("  - generate_review_post: Генерация поста с отзывом")
