from tinydb import TinyDB
from pathlib import Path
from validators import determine_field_type


class TemplateDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(db_path, encoding='utf-8')
        self.table = self.db.table('templates')

    def find_template(self, fields):
        templates = self.table.all()

        for template in templates:
            template_fields = {k: v for k, v in template.items() if k != 'name'}
            match = True

            for field, field_type in template_fields.items():
                if field not in fields:
                    match = False
                    break

                actual_type = determine_field_type(fields[field])
                if actual_type != field_type:
                    match = False
                    break

            if match:
                return template['name']

        return None

    def initialize_db(self):
        """Полная переинициализация базы данных"""
        # Закрываем текущее соединение
        self.db.close()

        # Удаляем файл базы данных, если он существует
        if Path(self.db_path).exists():
            Path(self.db_path).unlink()

        # Создаем новую базу
        self.db = TinyDB(self.db_path, encoding='utf-8')
        self.table = self.db.table('templates')

        # Добавляем тестовые данные
        self.table.insert_multiple([
            {
                "name": "Проба",
                "f_name1": "email",
                "f_name2": "date"
            },
            {
                "name": "Форма заказа",
                "customer": "text",
                "дата_заказа": "date"
            }
        ])

    def close(self):
        self.db.close()