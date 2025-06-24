import re
import argparse
from tinydb import TinyDB, Query

# Функции валидации типов полей
def is_date(value):
    date_patterns = [
        r'^\d{2}\.\d{2}\.\d{4}$',  # DD.MM.YYYY
        r'^\d{4}-\d{2}-\d{2}$'      # YYYY-MM-DD
    ]
    return any(re.match(pattern, value) for pattern in date_patterns)

def is_phone(value):
    phone_pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    return re.match(phone_pattern, value) is not None

def is_email(value):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, value) is not None

def detect_field_type(value):
    if is_date(value):
        return 'date'
    elif is_phone(value):
        return 'phone'
    elif is_email(value):
        return 'email'
    return 'text'

def find_matching_template(fields):
    db = TinyDB('db.json')
    templates = db.all()
    
    for template in templates:
        template_fields = {k: v for k, v in template.items() if k != 'name'}
        match = True
        
        for field_name, field_type in template_fields.items():
            if field_name not in fields or fields[field_name] != field_type:
                match = False
                break
                
        if match:
            return template['name']
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Find matching form template.')
    parser.add_argument('command', type=str, help='Command to execute (get_tpl)')
    parser.add_argument('fields', nargs='*', help='Form fields in format --name=value')
    
    args = parser.parse_args()
    
    if args.command != 'get_tpl':
        print("Unknown command. Use 'get_tpl'.")
        return
    
    # Парсинг полей из аргументов
    input_fields = {}
    detected_fields = {}
    
    for field in args.fields:
        if field.startswith('--'):
            field = field[2:]
            if '=' in field:
                name, value = field.split('=', 1)
                field_type = detect_field_type(value)
                input_fields[name] = field_type
                detected_fields[name] = field_type
    
    # Поиск подходящего шаблона
    template_name = find_matching_template(input_fields)
    
    if template_name:
        print(template_name)
    else:
        # Форматируем вывод как JSON-подобный словарь
        print('{')
        for i, (name, type_) in enumerate(detected_fields.items()):
            print(f'  {name}: {type_}' + (',' if i < len(detected_fields)-1 else ''))
        print('}')

if __name__ == '__main__':
    main()
