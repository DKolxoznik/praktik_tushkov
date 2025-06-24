from tinydb import TinyDB

def initialize_db():
    db = TinyDB('db.json')
    db.truncate()  # Очищаем базу
    
    # Добавляем тестовые шаблоны
    templates = [
        {
            "name": "Данные пользователя",
            "login": "email",
            "tel": "phone"
        },
        {
            "name": "Форма заказа",
            "customer": "text",
            "order_id": "text",
            "дата_заказа": "date",
            "contact": "phone"
        },
        {
            "name": "Проба",
            "f_name1": "email",
            "f_name2": "date"
        }
    ]
    
    for template in templates:
        db.insert(template)
    
    print("Database initialized with test templates.")

if __name__ == '__main__':
    initialize_db()
