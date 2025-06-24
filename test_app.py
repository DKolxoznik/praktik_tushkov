import pytest
import subprocess
from tinydb import TinyDB

@pytest.fixture(scope='module', autouse=True)
def setup_db():
    # Инициализация тестовой базы данных
    db = TinyDB('test_db.json')
    db.truncate()
    
    test_templates = [
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
    
    for template in test_templates:
        db.insert(template)
    
    yield
    
    # Удаляем тестовую базу после завершения тестов
    import os
    os.remove('test_db.json')

def test_is_date():
    from app import is_date
    assert is_date('31.12.2020') is True
    assert is_date('2020-12-31') is True
    assert is_date('31/12/2020') is False
    assert is_date('2020.12.31') is False

def test_is_phone():
    from app import is_phone
    assert is_phone('+7 123 456 78 90') is True
    assert is_phone('81234567890') is False
    assert is_phone('+7(123)456-78-90') is False

def test_is_email():
    from app import is_email
    assert is_email('test@example.com') is True
    assert is_email('user.name+tag@domain.co') is True
    assert is_email('not-an-email') is False
    assert is_email('missing@tld') is False

def test_detect_field_type():
    from app import detect_field_type
    assert detect_field_type('31.12.2020') == 'date'
    assert detect_field_type('2020-12-31') == 'date'
    assert detect_field_type('+7 123 456 78 90') == 'phone'
    assert detect_field_type('test@example.com') == 'email'
    assert detect_field_type('plain text') == 'text'

def test_find_matching_template():
    from app import find_matching_template
    db = TinyDB('test_db.json')
    
    # Тест на совпадение с шаблоном "Проба"
    fields = {'f_name1': 'email', 'f_name2': 'date'}
    assert find_matching_template(fields) == 'Проба'
    
    # Тест на совпадение с дополнительными полями
    fields = {'f_name1': 'email', 'f_name2': 'date', 'extra': 'text'}
    assert find_matching_template(fields) == 'Проба'
    
    # Тест на отсутствие совпадения
    fields = {'f_name1': 'email'}
    assert find_matching_template(fields) is None
    
    # Тест на другой шаблон
    fields = {'login': 'email', 'tel': 'phone'}
    assert find_matching_template(fields) == 'Данные пользователя'

def test_cli_matching_template():
    # Тестирование через командную строку
    result = subprocess.run(
        ['python', 'app.py', 'get_tpl', '--f_name1=test@test.com', '--f_name2=31.12.2020'],
        capture_output=True, text=True
    )
    assert 'Проба' in result.stdout

def test_cli_no_matching_template():
    result = subprocess.run(
        ['python', 'app.py', 'get_tpl', '--unknown=31.12.2020'],
        capture_output=True, text=True
    )
    assert 'unknown: date' in result.stdout

if __name__ == '__main__':
    pytest.main(["-v"])
