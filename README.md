# Form Template Finder

Приложение для поиска шаблонов форм по переданным полям и определения типов полей.

## 📦 Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/yourusername/form_template_app.git
cd form_template_app
```
2. Установите зависимости:

```
pip install tinydb
```
3. Инициализируйте базу данных:

```
python init_db.py
```
## 🚀 Использование
Поиск шаблона формы:
```
python app.py get_tp1 --field1=value1 --field2=value2
```
### Примеры:

```
# Найден шаблон
python app.py get_tp1 --f_name1=test@example.com --f_name2=01.01.2023
# Вывод: Проба

# Шаблон не найден (определение типов)
python app.py get_tp1 --unknown_field=01.01.2023
# Вывод: {'unknown_field': 'date'}
```
### Поддерживаемые типы полей:

- email (test@example.com)
- phone (+7 123 456 78 90)
- date (01.01.2023 или 2023-01-01)
- text (любые другие значения)

## 🧪 Тестирование
```
python tests.py
```
## 📁 Структура проекта
```
.
├── app.py               # Основной скрипт
├── database.py          # Работа с базой данных
├── validators.py        # Валидация типов полей
├── init_db.py           # Инициализация БД
├── tests.py             # Тесты
├── db.json              # Файл базы данных
└── README.md            # Этот файл
```