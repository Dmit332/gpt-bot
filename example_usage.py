"""
Примеры использования AI Real Estate Bot
Демонстрация основных возможностей системы
"""
import asyncio
from mcp_server import mcp_server
from ai_assistant import ai_assistant
from content_generator import content_generator


def example_1_add_properties():
    """Пример 1: Добавление объектов недвижимости"""
    print("\n=== Пример 1: Добавление объектов ===\n")
    
    properties = [
        {
            "title": "Современная 2-комнатная квартира в ЖК 'Парк Мира'",
            "type": "apartment",
            "price": 4500000,
            "location": "Москва, Северный округ, ул. Мира 125",
            "area": 65,
            "rooms": 2,
            "description": "Отличная квартира в новом ЖК с развитой инфраструктурой. Качественная отделка, панорамные окна, закрытая территория. Рядом парк, школа, детский сад, метро в 7 минутах.",
            "images": ["img1.jpg", "img2.jpg", "img3.jpg"]
        },
        {
            "title": "Просторная 3-комнатная с видом на реку",
            "type": "apartment",
            "price": 7200000,
            "location": "Москва, Центральный район, набережная Тараса Шевченко 23",
            "area": 92,
            "rooms": 3,
            "description": "Элитная квартира на 15 этаже с потрясающим видом на Москву-реку. Премиум отделка, кухня с техникой Miele, система умный дом. Охраняемая парковка.",
            "images": ["img4.jpg", "img5.jpg"]
        },
        {
            "title": "Уютная студия для молодой семьи",
            "type": "apartment",
            "price": 3200000,
            "location": "Москва, Западный округ, ул. Говорова 42",
            "area": 35,
            "rooms": 1,
            "description": "Идеальный вариант для первого жилья. Свежий ремонт, встроенная кухня, большая лоджия. Развитая инфраструктура, 10 минут до метро.",
            "images": ["img6.jpg"]
        },
        {
            "title": "Загородный дом с участком",
            "type": "house",
            "price": 12000000,
            "location": "Московская область, Одинцовский район, КП 'Зеленые холмы'",
            "area": 180,
            "rooms": 5,
            "description": "Современный дом 180 м² на участке 10 соток. Газ, свет, вода центральные. Закрытый поселок с охраной, детская площадка, озеро. 15 км от МКАД.",
            "images": ["img7.jpg", "img8.jpg", "img9.jpg", "img10.jpg"]
        },
        {
            "title": "Коммерческое помещение под офис",
            "type": "commercial",
            "price": 8500000,
            "location": "Москва, Деловой центр, ул. Пресненская набережная 10",
            "area": 120,
            "rooms": 4,
            "description": "Офисное помещение в бизнес-центре класса А. Отдельный вход, парковка, современная отделка. Идеально для IT-компании или консалтинга.",
            "images": ["img11.jpg", "img12.jpg"]
        }
    ]
    
    added_ids = []
    for prop in properties:
        result = mcp_server.add_property(**prop)
        added_ids.append(result['id'])
        print(f"✅ Добавлен объект: {prop['title']}")
        print(f"   ID: {result['id']}, Цена: {prop['price']:,} ₽\n")
    
    print(f"Всего добавлено: {len(added_ids)} объектов\n")
    return added_ids


def example_2_search_properties():
    """Пример 2: Поиск объектов по фильтрам"""
    print("\n=== Пример 2: Поиск объектов ===\n")
    
    # Поиск квартир до 5 млн
    print("🔍 Поиск: Квартиры до 5 млн рублей\n")
    results = mcp_server.search_properties({
        "type": "apartment",
        "max_price": 5000000
    })
    print(f"Найдено: {len(results)} объектов")
    for prop in results:
        print(f"  - {prop['title']} | {prop['price']:,} ₽")
    
    # Поиск в центре
    print("\n🔍 Поиск: Недвижимость в центре\n")
    results = mcp_server.search_properties({
        "location": "Центральный"
    })
    print(f"Найдено: {len(results)} объектов")
    for prop in results:
        print(f"  - {prop['title']} | {prop['location']}")
    
    # Поиск 3-комнатных
    print("\n🔍 Поиск: 3-комнатные квартиры\n")
    results = mcp_server.search_properties({
        "rooms": 3
    })
    print(f"Найдено: {len(results)} объектов")
    for prop in results:
        print(f"  - {prop['title']} | {prop['rooms']} комн., {prop['area']} м²")
    
    print()


async def example_3_chat_with_ai():
    """Пример 3: Диалог с AI-ассистентом"""
    print("\n=== Пример 3: Диалог с AI-ассистентом ===\n")
    
    client_id = "demo_client_001"
    
    messages = [
        "Привет! Хочу купить квартиру",
        "Ищу 2-комнатную в Москве",
        "Бюджет до 5 миллионов",
        "Желательно ближе к центру"
    ]
    
    for message in messages:
        print(f"👤 Клиент: {message}")
        response = await ai_assistant.process_message(client_id, message, "demo")
        print(f"🤖 Ассистент: {response}\n")
        await asyncio.sleep(1)  # Имитация естественной паузы


def example_4_create_client():
    """Пример 4: Создание клиента с предпочтениями"""
    print("\n=== Пример 4: Создание клиента ===\n")
    
    client = mcp_server.create_client(
        name="Иван Петров",
        phone="+79991234567",
        channel="whatsapp",
        preferences={
            "type": "apartment",
            "min_price": 3000000,
            "max_price": 5000000,
            "rooms": 2,
            "location": "Москва"
        }
    )
    
    print(f"✅ Создан клиент: {client['name']}")
    print(f"   ID: {client['id']}")
    print(f"   Телефон: {client['phone']}")
    print(f"   Канал: {client['channel']}")
    print(f"   Предпочтения: {client['preferences']}\n")
    
    # Обновление предпочтений
    print("🔄 Обновление предпочтений...\n")
    updated_prefs = {
        "type": "apartment",
        "min_price": 4000000,
        "max_price": 6000000,
        "rooms": 3,
        "location": "Москва, центр"
    }
    mcp_server.update_client_preferences(client['id'], updated_prefs)
    
    # Получение обновленных данных
    updated_client = mcp_server.get_client(client['id'])
    print(f"✅ Предпочтения обновлены: {updated_client['preferences']}\n")


def example_5_generate_content():
    """Пример 5: Генерация контента для соцсетей"""
    print("\n=== Пример 5: Генерация контента ===\n")
    
    # Получаем объекты
    properties = mcp_server.search_properties({"type": "apartment"})
    
    if not properties:
        print("⚠️  Сначала добавьте объекты (запустите example_1)")
        return
    
    # Генерируем пост об объекте
    print("📝 Генерация поста о квартире...\n")
    post_text = content_generator.generate_post_text(
        template_type="property_showcase",
        properties=[properties[0]]
    )
    print("=== ПОСТ ===")
    print(post_text)
    print("=" * 50 + "\n")
    
    # Генерируем сторис
    print("📸 Генерация текста для Stories...\n")
    story_text = content_generator.generate_story_text(properties[0])
    print("=== STORIES ===")
    print(story_text)
    print("=" * 50 + "\n")
    
    # Генерируем подборку
    if len(properties) >= 3:
        print("📋 Генерация подборки...\n")
        selection_post = content_generator.generate_post_text(
            template_type="selection",
            properties=properties[:3],
            topic="ТОП-3 квартиры этой недели"
        )
        print("=== ПОДБОРКА ===")
        print(selection_post)
        print("=" * 50 + "\n")


def example_6_content_pack():
    """Пример 6: Создание контент-пакета на месяц"""
    print("\n=== Пример 6: Контент-пакет на месяц ===\n")
    
    properties = mcp_server.search_properties({})
    
    if len(properties) < 3:
        print("⚠️  Для создания контент-пакета нужно минимум 3 объекта")
        print("   Запустите example_1 для добавления объектов\n")
        return
    
    print("🎨 Создание контент-пакета...")
    print("   Это может занять некоторое время...\n")
    
    pack = content_generator.create_content_pack(
        num_posts=5,  # 5 постов для демо
        num_stories=5  # 5 сторис для демо
    )
    
    print(f"✅ Контент-пакет создан!")
    print(f"   📝 Постов: {len(pack['posts'])}")
    print(f"   📸 Сторис: {len(pack['stories'])}")
    print(f"   📅 Записей в расписании: {len(pack['schedule'])}\n")
    
    # Показываем расписание
    print("📅 Расписание публикаций:")
    for item in pack['schedule'][:10]:  # Первые 10
        print(f"   {item['date']} | {item['type'].upper():7} | {item['title']}")
    
    if len(pack['schedule']) > 10:
        print(f"   ... и еще {len(pack['schedule']) - 10} записей")
    
    print()


def example_7_mcp_api():
    """Пример 7: Использование MCP API"""
    print("\n=== Пример 7: MCP API для n8n ===\n")
    
    from mcp_server import handle_mcp_request
    
    # Создание клиента через MCP
    print("📡 MCP Request: create_client\n")
    result = handle_mcp_request("create_client", {
        "name": "Мария Иванова",
        "phone": "+79997654321",
        "channel": "website"
    })
    print(f"✅ Ответ: {result}\n")
    
    # Поиск объектов через MCP
    print("📡 MCP Request: search_properties\n")
    result = handle_mcp_request("search_properties", {
        "type": "apartment",
        "max_price": 5000000
    })
    print(f"✅ Найдено объектов: {len(result)}")
    for prop in result[:3]:
        print(f"   - {prop['title']}")
    print()
    
    # Получение расписания контента
    print("📡 MCP Request: get_content_schedule\n")
    result = handle_mcp_request("get_content_schedule", {"limit": 5})
    print(f"✅ Расписание на ближайшие дни: {len(result)} записей\n")


def run_all_examples():
    """Запустить все примеры"""
    print("\n" + "="*60)
    print("🏠 AI REAL ESTATE BOT - ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ")
    print("="*60)
    
    # Пример 1: Добавление объектов
    example_1_add_properties()
    
    # Пример 2: Поиск
    example_2_search_properties()
    
    # Пример 3: AI-ассистент (асинхронный)
    asyncio.run(example_3_chat_with_ai())
    
    # Пример 4: Клиенты
    example_4_create_client()
    
    # Пример 5: Генерация контента
    example_5_generate_content()
    
    # Пример 6: Контент-пакет
    example_6_content_pack()
    
    # Пример 7: MCP API
    example_7_mcp_api()
    
    print("\n" + "="*60)
    print("✅ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ!")
    print("="*60 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        examples = {
            "1": example_1_add_properties,
            "2": example_2_search_properties,
            "3": lambda: asyncio.run(example_3_chat_with_ai()),
            "4": example_4_create_client,
            "5": example_5_generate_content,
            "6": example_6_content_pack,
            "7": example_7_mcp_api
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Пример {example_num} не найден")
            print("Доступные примеры: 1-7 или запустите без аргументов для всех")
    else:
        # Запускаем все примеры
        run_all_examples()
