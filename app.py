import argparse
from database import TemplateDB


def get_tp1():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser()
    args, unknown = parser.parse_known_args()

    # Извлекаем параметры вида --ключ=значение
    fields = {}
    for arg in unknown:
        if arg.startswith('--'):
            key_value = arg[2:].split('=', 1)
            if len(key_value) == 2:
                fields[key_value[0]] = key_value[1]

    # Работаем с базой данных
    db = TemplateDB('db.json')
    try:
        template_name = db.find_template(fields)

        if template_name:
            print(template_name)
        else:
            # Определяем типы полей
            from validators import determine_field_type
            field_types = {field: determine_field_type(value) for field, value in fields.items()}
            print(field_types)
    finally:
        db.close()


if __name__ == '__main__':
    get_tp1()