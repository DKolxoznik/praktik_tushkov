from database import TemplateDB

def initialize_database():
    db = TemplateDB('db.json')
    try:
        db.initialize_db()
        print("✅ База данных успешно инициализирована")
        print(f"📁 Файл базы данных: db.json")
    finally:
        db.close()

if __name__ == '__main__':
    initialize_database()