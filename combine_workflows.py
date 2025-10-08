#!/usr/bin/env python3
"""
Скрипт для объединения всех workflows в один файл
"""
import json

# Список файлов workflows
workflow_files = [
    'n8n_workflow_1_new_lead.json',
    'n8n_workflow_2_property_search.json',
    'n8n_workflow_3_content_schedule.json',
    'n8n_workflow_4_whatsapp_ai.json',
    'n8n_workflow_5_content_pack.json',
    'n8n_workflow_6_hot_leads.json'
]

# Объединяем все workflows
all_workflows = []

for filename in workflow_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
            all_workflows.append(workflow)
            print(f"✓ Загружен: {workflow.get('name', filename)}")
    except Exception as e:
        print(f"✗ Ошибка при загрузке {filename}: {e}")

# Сохраняем объединенный файл
output_file = 'n8n_ALL_WORKFLOWS.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_workflows, f, ensure_ascii=False, indent=2)

print(f"\n✅ Создан файл: {output_file}")
print(f"📦 Всего workflows: {len(all_workflows)}")
print(f"\nТеперь импортируйте {output_file} в n8n!")
