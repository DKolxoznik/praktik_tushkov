import re
from datetime import datetime

def is_date(value):
    try:
        datetime.strptime(value, '%d.%m.%Y')
        return True
    except ValueError:
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

def is_phone(value):
    return re.fullmatch(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value) is not None

def is_email(value):
    return re.fullmatch(r'^[^@]+@[^@]+\.[^@]+$', value) is not None

def determine_field_type(value):
    if is_date(value):
        return 'date'
    elif is_phone(value):
        return 'phone'
    elif is_email(value):
        return 'email'
    return 'text'